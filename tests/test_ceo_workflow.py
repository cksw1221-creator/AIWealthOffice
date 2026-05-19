from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ga_multica.models import CommandResult

from ga_multica.ceo import dispatch_issue, load_worker_registry, resolve_worker
from ga_multica.polling import format_issue_summary, poll_issue


def command_result(payload: object) -> CommandResult:
    return CommandResult(
        args=("multica",),
        returncode=0,
        stdout=json.dumps(payload),
        stderr="",
        parsed=payload,
    )


class FakeDispatchClient:
    def __init__(self) -> None:
        self.create_calls: list[dict[str, object]] = []
        self.comment_calls: list[dict[str, object]] = []
        self.status_calls: list[dict[str, object]] = []

    def issue_create(self, title: str, **kwargs: object) -> CommandResult:
        description_path = Path(str(kwargs["description_file"]))
        self.create_calls.append(
            {
                "title": title,
                "description": description_path.read_text(encoding="utf-8"),
                **kwargs,
            }
        )
        return command_result({"id": "issue-123", "identifier": "AIW-123", "title": title})

    def issue_comment_add(self, issue_id: str, **kwargs: object) -> CommandResult:
        content_path = Path(str(kwargs["content_file"]))
        self.comment_calls.append(
            {
                "issue_id": issue_id,
                "content": content_path.read_text(encoding="utf-8"),
                **kwargs,
            }
        )
        return command_result({"id": "comment-1", "issue_id": issue_id})

    def issue_status(self, issue_id: str, status: str) -> CommandResult:
        self.status_calls.append({"issue_id": issue_id, "status": status})
        return command_result({"id": issue_id, "status": status})


class FakePollingClient:
    def issue_get(self, issue_id: str) -> CommandResult:
        return command_result(
            {
                "id": issue_id,
                "identifier": "AIW-4",
                "title": "Build CEO scripts",
                "status": "in_progress",
                "updated_at": "2026-05-19T00:00:00Z",
                "assignee_id": "agent-1",
            }
        )

    def issue_runs(self, issue_id: str) -> CommandResult:
        return command_result(
            [
                {
                    "id": "run-1",
                    "status": "completed",
                    "attempt": 1,
                    "agent_id": "agent-1",
                    "started_at": "2026-05-19T00:01:00Z",
                    "completed_at": "2026-05-19T00:03:00Z",
                },
                {
                    "id": "run-2",
                    "status": "running",
                    "attempt": 2,
                    "agent_id": "agent-2",
                    "started_at": "2026-05-19T00:04:00Z",
                    "completed_at": None,
                },
            ]
        )

    def issue_run_messages(self, task_id: str, **kwargs: object) -> CommandResult:
        self.last_message_request = {"task_id": task_id, **kwargs}
        return command_result(
            [
                {"seq": 10, "type": "tool_use", "input": {"command": "multica issue get AIW-4"}},
                {
                    "seq": 11,
                    "type": "tool_result",
                    "output": "token=super-secret-value should be hidden",
                },
                {"seq": 12, "type": "text", "content": "Latest worker update from the coder."},
            ]
        )


class WorkerRegistryTests(unittest.TestCase):
    def test_load_and_resolve_worker_by_name_and_id(self) -> None:
        registry = {
            "workers": {
                "Coder-gpt-5.4-high-Builder": {"agent_id": "agent-123", "role": "Coder"},
                "Coder-gpt-5.4-medium-Builder": {"agent_id": "agent-456", "role": "Coder"},
            }
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "worker_registry.json"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")

            loaded = load_worker_registry(registry_path)
            self.assertEqual(resolve_worker(loaded, "Coder-gpt-5.4-high-Builder")["agent_id"], "agent-123")
            self.assertEqual(resolve_worker(loaded, "agent-456")["name"], "Coder-gpt-5.4-medium-Builder")


class DispatchAndReviewTests(unittest.TestCase):
    def test_dispatch_issue_uses_registry_resolution_and_utf8_temp_file(self) -> None:
        registry = {
            "workers": {
                "Coder-gpt-5.4-high-Builder": {"agent_id": "agent-123", "role": "Coder"},
            }
        }
        client = FakeDispatchClient()
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "worker_registry.json"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")

            result = dispatch_issue(
                client,
                title="Implement CEO flow",
                description="CEO task body with unicode: 测试",
                worker_ref="Coder-gpt-5.4-high-Builder",
                registry_path=registry_path,
                priority="high",
                status="todo",
            )

        self.assertEqual(result["identifier"], "AIW-123")
        self.assertEqual(client.create_calls[0]["assignee_id"], "agent-123")
        self.assertEqual(client.create_calls[0]["description"], "CEO task body with unicode: 测试")

    def test_review_issue_posts_comment_then_updates_status(self) -> None:
        from ga_multica.ceo import review_issue

        client = FakeDispatchClient()
        result = review_issue(client, issue_id="AIW-4", comment="Please tighten the docs.", status="todo")

        self.assertEqual(result["status"]["status"], "todo")
        self.assertEqual(client.comment_calls[0]["content"], "Please tighten the docs.")
        self.assertEqual(client.status_calls[0]["status"], "todo")


class PollingTests(unittest.TestCase):
    def test_poll_issue_summarizes_latest_run_and_message(self) -> None:
        client = FakePollingClient()

        summary = poll_issue(client, "AIW-4", since_seq=9)

        self.assertEqual(summary["issue"]["identifier"], "AIW-4")
        self.assertEqual(summary["latest_run"]["id"], "run-2")
        self.assertEqual(summary["latest_run"]["status"], "running")
        self.assertEqual(summary["last_message"]["seq"], 12)
        self.assertEqual(summary["last_message"]["preview"], "Latest worker update from the coder.")
        self.assertEqual(client.last_message_request["since"], 9)

    def test_format_issue_summary_is_human_readable_and_redacted(self) -> None:
        client = FakePollingClient()
        summary = poll_issue(client, "AIW-4")

        text = format_issue_summary(summary)

        self.assertIn("Issue AIW-4: Build CEO scripts", text)
        self.assertIn("Latest run: running", text)
        self.assertIn("Latest worker update from the coder.", text)
        self.assertNotIn("super-secret-value", text)


if __name__ == "__main__":
    unittest.main()

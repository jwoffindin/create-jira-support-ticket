from os import path
from dataclasses import dataclass
from typing import Dict, List

from jira.resources import Issue
import jinja2

from . import jira

@dataclass
class SupportTicket:
    """Create a support ticket in JIRA"""
    TEMPLATE_DIR = path.join(
        path.dirname(path.abspath(__file__)), "templates"
    )

    project: str
    work_type: str
    labels: List[str]
    summary: str
    epic: Issue

    def raise_issue(self) -> Issue:
        """Create issue in jira"""

        fields = self._fields()
        issue = jira.create_issue(fields=fields)

        issue = jira.create_issue(fields=fields)
        if "parent" not in fields:
            jira.create_issue_link(type="relates to", inwardIssue=issue.key, outwardIssue=self.epic.key, comment={'body': "Associated with epic {self.epic.key}"})

        return issue

    def _fields(self) -> Dict:
        fields = {
            "project": {"key": self.project},
            "summary": self._summary(),
            "description": self._description(),
            "issuetype": {"name": self._issue_type()},
            "labels": self._labels(),
            "assignee": {'accountId': jira.current_user()},
            "components": [{ "name": component } for component in self._components()],
        }

        # If the epic is in the same project as the issue, set the parent to the epic; otherwise we'll just link the issue once it's created
        if self._project_key(self.epic) == self.project:
            fields["parent"] = {"key": self.epic.key}

        return fields

    def _project_key(self, issue: Issue) -> str:
        """returns project key for JIRA issue"""
        return issue.key[:issue.key.index("-")]

    def _summary(self) -> str:
        """Builds up summary for JIRA issue, including value stream if it's tagged as a component"""
        summary = ""
        components = self._components()
        if len(components) == 1:
            summary = f"[{components[0]}] : "
        return summary + self.summary

    def _issue_type(self) -> str:
        """returns ID for JIRA issue type"""
        return "Task"

    def _labels(self) -> List[str]:
        """returns labels for jira issue"""
        return self.labels + ["support-request"]

    def _description(self) -> str:
        return self._read_template(
            f"{self.work_type}.md",
            epic=self.epic,
        )

    def _components(self) -> List[str]:
        return [ component.name for component in self.epic.fields.components ]

    def _read_template(self, *p: List[str], **params: Dict) -> str:
        """Read a template file, passing interpolation variables as optional named params"""
        environment = jinja2.Environment()

        with open(path.join(self.TEMPLATE_DIR, *p), "r", encoding="utf-8") as tpl:
            template = environment.from_string(tpl.read())

        rendered = template.render(**params)

        return rendered

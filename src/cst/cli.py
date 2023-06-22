#!/usr/bin/env python3

"""
Create JIRA ticket for support requests
"""

import datetime
import json
import re
import sys
import os

import click

from . import jira, JIRA_SERVER
from .support_ticket import SupportTicket

WORKTYPE__BUG = "bug"
WORKTYPE__SUPPORT = "support"
WORKTYPE__SECURITY = "security"

@click.command()
@click.argument("epic", type=click.STRING, required=True)
@click.argument("summary", nargs=-1, required=True)
@click.option(
    "--work-type",
    "-w",
    type=click.Choice(
        [
            WORKTYPE__BUG,
            WORKTYPE__SUPPORT,
            WORKTYPE__SECURITY,
        ],
        case_sensitive=True,
    ),
    default=WORKTYPE__SUPPORT,
)
@click.option("--labels", "-l", help="Comma separated list of labels")
@click.option("--project", "-p", help="Project to create issue in (defaults to epic project)")
def create_issue(epic, summary, work_type, labels, project):
    """Creates a JIRA support issue"""
    epic_issue = jira.issue(epic)
    print(epic_issue.fields.summary)

    if epic_issue.fields.issuetype.name != "Feature":
        print(f"Epic is incorrect issue type {epic_issue.fields.issuetype.name}, expected to be Feature")
        sys.exit(1)

    if not confirm():
        print("Exiting...")
        sys.exit(0)

    # Project defaults to same project as epic.
    if not project:
        project = epic[:epic.index("-")]

    issue = SupportTicket(
        project=project,
        epic=epic_issue,
        summary=" ".join(summary),
        work_type=work_type,
        labels=(labels.split(",") if labels else []),
    ).raise_issue()

    print(f"Issue at: {JIRA_SERVER + ('/' if not JIRA_SERVER.endswith('/') else '')}browse/{issue.key}")

def confirm():
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("continue [Y/N]? ").lower()
    return answer == "y"


if __name__ == "__main__":
    create_issue()

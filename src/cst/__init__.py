"""
Simple CLI for creating JIRA tickets from the command line.
"""
import os
from jira import JIRA

VERSION = "0.0.1"

JIRA_SERVER = os.environ["JIRA_SERVER"]
JIRA_USERNAME = os.environ["JIRA_USERNAME"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]

jira = JIRA(options={"server": JIRA_SERVER}, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))


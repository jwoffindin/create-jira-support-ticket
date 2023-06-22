# `cst` - Create JIRA tickets for support requests

Create JIRA tickets for support requests.

Support requests are linked back to a parent "epic" ticket (actually a "Feature" type).

JIRA **components** are used to track which team the support ticket is associated with. These will be copied from the parent epic ticket automatically.

## Installation

## Usage

```
$ cst --help
Usage: cst [OPTIONS] EPIC SUMMARY...

  Creates a JIRA support issue based on provided args

Options:
  -w, --work-type [bug|support|security]
  -l, --labels TEXT               Comma separated list of labels
  -p, --project TEXT              Project to create issue in (defaults to epic
                                  project)
  --help                          Show this message and exit.

```

## Examples

```
cst MY-123 -- Request to do X
```

will create a _Task_ ticket with the summary "Request to do X" and link it to the epic ticket MY-123.

```
cst MY-123 -w bug -- Fix Y
```

creates a _Bug_ ticket with the summary "Fix Y" and links it to the epic ticket MY-123.

```
cst AB-999 -p XY -- Support to do Z
```

creates a _Task_ ticket in project `XY` linked back to the epic ticket AB-999.

## Templates

Templates are used to generate the JIRA ticket description.

The template is a Jinja2 template, and the context is the command line arguments.

These templates should be updated to be something more useful, especially the bug template.

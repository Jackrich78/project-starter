# Variables & Templating Guide

**Dynamic Block Kit JSON with N8N and Python**

This guide explains how to use dynamic data in Block Kit JSON. The Skill generates templates; you substitute variables at runtime.

---

## Important Clarification

**This Skill generates TEMPLATE placeholders only.** Variable substitution happens outside the Skill:

1. **Skill's job:** Generate JSON with placeholder syntax (e.g., `{{$node.data}}` or `{variable}`)
2. **Your job:** Substitute real values at runtime (N8N engine or Python code)

The Skill shows you *how* to format placeholders and provides examples, but does NOT perform the substitution.

---

## N8N Variable Substitution

### N8N Jinja2 Template Syntax

**Format:** `{{$node.NODE_NAME.data.FIELD_NAME}}`

**Example:**
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Request from: {{$node.TriggerData.data.requester_name}}"
  }
}
```

When N8N workflow runs:
- N8N engine parses `{{...}}` syntax
- Looks up `TriggerData` node output
- Gets the `requester_name` field
- Substitutes into the JSON

**Result:**
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Request from: Alice Smith"
  }
}
```

### N8N Reference Syntax Patterns

**Basic field reference:**
```
{{$node.NodeName.data.fieldName}}
```

**Nested field:**
```
{{$node.NodeName.data.parent.child}}
```

**Array index:**
```
{{$node.NodeName.data.items[0]}}
```

**With formatting:**
```
{{$node.NodeName.data.amount | formatMoney}}
```

### N8N Workflow Example

**Scenario:** Bot sends budget approval request with dynamic data from previous node

**Previous Node Output:**
```json
{
  "requester": "John Doe",
  "amount": 5000,
  "department": "Marketing",
  "purpose": "Q4 Campaign"
}
```

**N8N Slack Node JSON:**
```json
{
  "text": "Budget approval needed",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Budget Approval Request"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Requester:*\n{{$node.GetRequest.data.requester}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Amount:*\n${{$node.GetRequest.data.amount}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Department:*\n{{$node.GetRequest.data.department}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Purpose:*\n{{$node.GetRequest.data.purpose}}"
        }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Approve" },
          "value": "approve",
          "action_id": "approve_{{$node.GetRequest.data.request_id}}"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Deny" },
          "value": "deny",
          "action_id": "deny_{{$node.GetRequest.data.request_id}}"
        }
      ]
    }
  ]
}
```

**When N8N runs this workflow:**
1. GetRequest node fetches data
2. Slack node receives JSON with `{{...}}` placeholders
3. N8N engine substitutes all variables
4. Message posts to Slack with real data

**Result in Slack:**
```
Budget Approval Request

Requester: John Doe
Amount: $5000

Department: Marketing
Purpose: Q4 Campaign

[Approve] [Deny] buttons
```

---

## Python Variable Substitution

### Python f-Strings (Recommended for Modern Python 3.6+)

**Format:** `f"text {variable}"`

**Syntax:**
```python
user_name = "Alice Smith"
task_title = "Complete Report"

block = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": f"*Task for:* {user_name}\n*Title:* {task_title}"
    }
}
```

**Features:**
- Readable and modern
- Expression evaluation: `f"{amount * 1.1}"`
- Format specifiers: `f"{date:.2f}"`

### Python .format() Method

**Format:** `"text {}".format(variable)`

**Syntax:**
```python
user_name = "Alice Smith"
task_title = "Complete Report"

block = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Task for:* {}\n*Title:* {}".format(user_name, task_title)
    }
}
```

**Features:**
- Compatible with Python 2.7+
- Positional or named placeholders
- Format specifiers supported

### Python Jinja2 Template Library

**Format:** `render with Jinja2 engine`

**Syntax:**
```python
from jinja2 import Template

template_str = '''
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Task for:* {{ user_name }}\\n*Title:* {{ task_title }}"
  }
}
'''

template = Template(template_str)
json_str = template.render(user_name="Alice", task_title="Report")
json_obj = json.loads(json_str)
```

**Features:**
- Separate templates from code
- Complex logic (loops, conditionals)
- Reusable templates

---

## Complete Python Examples

### Example 1: F-String with slack_sdk

```python
from slack_sdk import WebClient

# Initialize client
client = WebClient(token="xoxb-your-token")

# Data
user_name = "Alice Smith"
request_title = "Budget Approval"
amount = 5000
urgency = "High"

# Generate JSON with f-strings
blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": request_title
        }
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": f"*Requester:*\n{user_name}"
            },
            {
                "type": "mrkdwn",
                "text": f"*Amount:*\n${amount:,}"
            },
            {
                "type": "mrkdwn",
                "text": f"*Urgency:*\n{urgency}"
            }
        ]
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": { "type": "plain_text", "text": "Approve" },
                "value": "approve",
                "action_id": "approve_action"
            },
            {
                "type": "button",
                "text": { "type": "plain_text", "text": "Deny" },
                "value": "deny",
                "action_id": "deny_action"
            }
        ]
    }
]

# Post message
response = client.chat_postMessage(
    channel="C1234567890",
    text="Budget approval request",
    blocks=blocks
)

print(f"Message sent: {response['ts']}")
```

### Example 2: .format() Method

```python
from slack_sdk import WebClient
import json

client = WebClient(token="xoxb-your-token")

# Data
user_name = "Bob Johnson"
task_title = "Q4 Report"
due_date = "2025-11-30"

# JSON template with .format()
json_template = '''
{{
  "type": "section",
  "text": {{
    "type": "mrkdwn",
    "text": "*Task:* {}\\n*Assigned to:* {}\\n*Due:* {}"
  }},
  "accessory": {{
    "type": "button",
    "text": {{ "type": "plain_text", "text": "Complete" }},
    "value": "complete",
    "action_id": "complete_task",
    "style": "primary"
  }}
}}
'''

# Substitute variables
json_str = json_template.format(task_title, user_name, due_date)
block = json.loads(json_str)

# Post
response = client.chat_postMessage(
    channel="C1234567890",
    text="Task assignment",
    blocks=[block]
)
```

### Example 3: Jinja2 Template for Reusability

```python
from slack_sdk import WebClient
from jinja2 import Template
import json

client = WebClient(token="xoxb-your-token")

# Reusable template
approval_template = Template('''
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Approval Needed*\\n\\nRequester: {{ requester }}\\nAmount: ${{ amount }}\\nReason: {{ reason }}"
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "Review" },
    "url": "https://example.com/approval/{{ request_id }}"
  }
}
''')

# Use template with different data
requests = [
    {"requester": "Alice", "amount": 1000, "reason": "Software", "request_id": "REQ001"},
    {"requester": "Bob", "amount": 500, "reason": "Hardware", "request_id": "REQ002"},
]

for req in requests:
    json_str = approval_template.render(**req)
    block = json.loads(json_str)

    client.chat_postMessage(
        channel="C1234567890",
        text="Approval request",
        blocks=[block]
    )
```

---

## Variable Placement in Block Kit

### Text Objects (mrkdwn)
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Hello {{$node.name}} - your balance is {{$node.balance}}"
  }
}
```

### Field Values
```json
{
  "type": "section",
  "fields": [
    { "type": "mrkdwn", "text": "*Status:*\n{{$node.status}}" },
    { "type": "mrkdwn", "text": "*Date:*\n{{$node.date}}" }
  ]
}
```

### Button Text
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "{{$node.button_label}}" },
  "action_id": "button_{{$node.id}}"
}
```

### URL Fields
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Open" },
  "url": "https://example.com/item/{{$node.item_id}}"
}
```

### Option Values
```json
{
  "type": "static_select",
  "options": [
    { "text": { "type": "plain_text", "text": "{{$node.option1_name}}" }, "value": "{{$node.option1_value}}" },
    { "text": { "type": "plain_text", "text": "{{$node.option2_name}}" }, "value": "{{$node.option2_value}}" }
  ],
  "action_id": "select_action"
}
```

---

## Common Pitfalls

### Pitfall 1: JSON Escaping in Strings
**Problem:** Text contains quotes that break JSON

**Solution:** Use newlines instead of escape sequences

**Wrong:**
```json
"text": "He said \"hello\""
```

**Right:**
```json
"text": "He said hello"
```

### Pitfall 2: Variables in Plain Text Objects
**Problem:** Using Jinja2 in `plain_text` (only works in `mrkdwn`)

**Wrong:**
```json
{
  "type": "plain_text",
  "text": "Hello {{$node.name}}"
}
```

**Right:**
```json
{
  "type": "mrkdwn",
  "text": "Hello {{$node.name}}"
}
```

### Pitfall 3: N8N Syntax Errors
**Problem:** Referencing non-existent node or field

**Solution:** Check exact node name and output structure

**Wrong:**
```
{{$node.GetUser.data.full_name}}  // If GetUser outputs user.name not full_name
```

**Right:**
```
{{$node.GetUser.data.user.name}}  // Check actual output structure
```

### Pitfall 4: Missing Escaping in N8N
**Problem:** Special characters in variables break JSON

**Solution:** N8N handles escaping, but test first

**Example:** If requester_name contains quotes, N8N should escape it.

---

## Testing Your Variables

### N8N: Enable JSON Preview
1. Click Slack node
2. Look for "Test" or preview pane
3. Run workflow with test data
4. Check that variables substituted correctly

### Python: Print JSON Before Sending
```python
import json

# Generate blocks
blocks = [...]

# Print JSON to verify
print(json.dumps(blocks, indent=2))

# Then send
client.chat_postMessage(channel="...", blocks=blocks)
```

### Block Kit Builder: Test the Result
1. Copy generated JSON (with real values, not placeholders)
2. Paste into Block Kit Builder
3. Verify rendering

---

## Tips for Success

1. **Use Block Kit Builder to prototype** - Test structure before adding variables
2. **Test with real data** - Use actual variable values when testing
3. **Check variable syntax** - Verify exact node names and field paths (especially N8N)
4. **Use mrkdwn for formatted text** - Only mrkdwn type supports variable substitution with formatting
5. **Print/preview before sending** - Debug variable output before posting to Slack
6. **Keep variable names short** - Readability in JSON files

---

## Reference Links

- **Block Kit Builder:** https://api.slack.com/tools/block-kit-builder
- **N8N Docs:** https://docs.n8n.io/
- **Slack SDK for Python:** https://slack.dev/python-slack-sdk/
- **Jinja2 Documentation:** https://jinja.palletsprojects.com/

---

**Next:** See [examples.md](examples.md) for complete real-world examples with variables, or [best-practices.md](best-practices.md) for validation checklists.

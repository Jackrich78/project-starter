# Slack Block Kit Claude Skill

**Purpose:** Generate valid Slack Block Kit JSON for messages, modals, and home tabs using conversational descriptions.

**Scope:** All 13 official Slack Block Kit block types, three surfaces (messages/modals/home tabs), N8N Jinja2 and Python variable templating.

**Version:** 1.0
**Status:** Production
**Last Updated:** 2025-11-20

---

## Quick Start

### Message (Notification)
**You:** "Create a notification message with title 'Alert', description 'System maintenance', and a link button."

**Skill generates:**
```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Alert*\nSystem maintenance"
      },
      "accessory": {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "Learn More"
        },
        "url": "https://example.com"
      }
    }
  ]
}
```

### Modal (Form)
**You:** "Create an approval modal with fields for requester name, amount, and urgency dropdown (Low/Medium/High). Include Approve and Deny buttons."

**Skill generates:**
```json
{
  "type": "modal",
  "callback_id": "approval_form",
  "title": {
    "type": "plain_text",
    "text": "Approval Request"
  },
  "submit": {
    "type": "plain_text",
    "text": "Approve"
  },
  "close": {
    "type": "plain_text",
    "text": "Deny"
  },
  "blocks": [
    {
      "type": "input",
      "block_id": "requester_input",
      "label": {
        "type": "plain_text",
        "text": "Requester Name"
      },
      "element": {
        "type": "plain_text_input",
        "action_id": "requester_action"
      }
    },
    {
      "type": "input",
      "block_id": "amount_input",
      "label": {
        "type": "plain_text",
        "text": "Amount"
      },
      "element": {
        "type": "plain_text_input",
        "action_id": "amount_action"
      }
    },
    {
      "type": "input",
      "block_id": "urgency_input",
      "label": {
        "type": "plain_text",
        "text": "Urgency"
      },
      "element": {
        "type": "static_select",
        "action_id": "urgency_action",
        "options": [
          {
            "text": {
              "type": "plain_text",
              "text": "Low"
            },
            "value": "low"
          },
          {
            "text": {
              "type": "plain_text",
              "text": "Medium"
            },
            "value": "medium"
          },
          {
            "text": {
              "type": "plain_text",
              "text": "High"
            },
            "value": "high"
          }
        ]
      }
    }
  ]
}
```

### Home Tab (Dashboard)
**You:** "Create a home tab dashboard showing recent tasks with a welcome header and settings button."

**Skill generates dashboard structure with header, task sections, and navigation.**

---

## How This Skill Works

### Step 1: Describe What You Want
Tell the Skill what you need in plain English. Include:
- **Surface:** Message, modal, or home tab
- **Content:** Headers, text, images, forms, buttons
- **Variables:** For N8N Jinja2 or Python substitution (optional)
- **Style:** Markdown formatting, colors, emphasis

**Examples:**
- "Create a message with a title and two buttons"
- "Generate a modal for collecting feedback with text area and submit"
- "Build a home tab showing user profile and recent activity"

### Step 2: Skill Generates JSON
The Skill produces syntactically valid Block Kit JSON ready to:
- Paste into Block Kit Builder for testing
- Use in N8N workflows with variable substitution
- Integrate into Python code with string templating

### Step 3: Validate & Deploy
- **Test:** Copy JSON into [Block Kit Builder](https://api.slack.com/tools/block-kit-builder) (free tool)
- **Integrate:** Use in N8N or Python following variable guidance
- **Deploy:** Post to Slack with dynamic content

---

## Reference Documentation

The Skill has 7 supporting reference docs for in-depth guidance:

### Core References
1. **[blocks-reference.md](docs/blocks-reference.md)** - All 13 block types with syntax and examples
   - When to use each block type
   - Required and optional fields
   - Common patterns

2. **[elements-guide.md](docs/elements-guide.md)** - Interactive elements (buttons, inputs, selects, etc.)
   - Element types and their block containers
   - Configuration options
   - Event handling patterns

3. **[composition-objects.md](docs/composition-objects.md)** - Building blocks for blocks
   - Text objects (plain_text vs mrkdwn)
   - Option lists for menus
   - Confirm dialogs for destructive actions

### Specification Guides
4. **[surfaces.md](docs/surfaces.md)** - Detailed specifications for each surface
   - Message surface: 50-block limit, display-focused
   - Modal surface: 100-block limit, form-focused
   - Home Tab surface: 100-block limit, persistent dashboard

5. **[variables-and-templating.md](docs/variables-and-templating.md)** - Variable substitution patterns
   - N8N Jinja2: `{{$node.data.field}}`
   - Python f-strings: `f"text {variable}"`
   - Python .format(): `"text {}".format(variable)`

### Examples & Best Practices
6. **[examples.md](docs/examples.md)** - Real-world use case examples
   - Approval workflows
   - Notifications and alerts
   - Task management dashboards
   - Feedback forms
   - User surveys

7. **[best-practices.md](docs/best-practices.md)** - Quality, accessibility, validation
   - JSON validation checklist
   - Accessibility guidelines
   - Common mistakes and fixes
   - Performance optimization

---

## Common Tasks

### Task: Generate JSON with Variables (N8N)
**You:** "Create a notification with N8N variables for username and task title. Use Jinja2 syntax."

**What the Skill does:**
1. Generates base Block Kit JSON structure
2. Includes N8N Jinja2 variable syntax: `{{$node.xxx}}`
3. Shows example substituted result
4. Explains that N8N engine substitutes variables at runtime

**Result:** JSON ready to paste into N8N Slack node

### Task: Generate Python Code with Variables
**You:** "Show me Python code that generates a task message using f-strings for title and due_date."

**What the Skill does:**
1. Generates Block Kit JSON structure
2. Provides Python code example with f-string placeholders
3. Shows .format() alternative method
4. Includes example using test data

**Result:** Executable Python code that generates valid Block Kit JSON

### Task: All 13 Block Types
**You:** "Show me examples of all 13 Slack Block Kit block types."

**What the Skill does:**
1. Lists all 13 official block types
2. References supporting docs for each
3. Generates example JSON for requested types
4. Explains when to use each

**Block types covered:**
- section, header, image, video, markdown, rich_text, divider, context, file, table, actions, input, context_actions

### Task: Verify Block Kit Validity
**You:** "Is this JSON valid for Block Kit?"

**What the Skill does:**
1. Checks syntax (valid JSON)
2. Validates structure (required fields present)
3. Checks surface compatibility (blocks valid for message/modal/home tab)
4. Suggests improvements if needed
5. Provides Block Kit Builder link for testing

---

## Important Concepts

### Blocks vs Elements
**Blocks** are containers (section, input, actions). **Elements** are interactive components (buttons, select menus, date pickers) that live *inside* blocks.

→ See [elements-guide.md](docs/elements-guide.md)

### Surface Limitations
- **Messages:** Up to 50 blocks, display-focused, no input blocks
- **Modals:** Up to 100 blocks, form-focused, input blocks allowed
- **Home Tabs:** Up to 100 blocks, persistent dashboard, limited interaction

→ See [surfaces.md](docs/surfaces.md)

### Variable Substitution
This Skill generates **template placeholders** only. Variable substitution happens *outside* the Skill:
- N8N substitutes at workflow runtime
- Python substitutes when code executes
- The Skill shows you how to format placeholders

→ See [variables-and-templating.md](docs/variables-and-templating.md)

### v1 Limitations
- **Single-step modals only** (no view stacking with previous_view_id)
- **No action/button handling code** (Skill generates JSON structure only; you handle responses in your app)
- **No interactive app workflows** (that's for your backend code)

---

## Troubleshooting

### "I got an error when I pasted the JSON into Block Kit Builder"
1. **Syntax error:** Check for missing commas, quotes, or brackets
2. **Invalid block type:** Verify block type is one of the 13 official types
3. **Wrong surface:** Check that blocks are valid for message/modal/home tab context
4. **Missing required fields:** All blocks need specific required fields

→ Copy the error message and ask the Skill to fix it

### "The variables aren't working in N8N"
1. **Jinja2 syntax:** Verify format is `{{$node.xxx.data.field}}`
2. **Node reference:** Check that the node name matches your workflow
3. **Data path:** Verify the data field exists in the output
4. **Timing:** Ensure the source node runs before the Slack node

→ The Skill generates templates; N8N does the substitution

### "I want to create a multi-step modal"
This is a v2 feature (modal view stacking with `previous_view_id`). For v1:
1. Use a single-step modal with all fields
2. Split into sequential modals (user submits, you show next modal)
3. Use home tab dashboard instead of modal flow

---

## Integration Examples

### N8N Workflow
1. Use Skill to generate Block Kit JSON with Jinja2 variables
2. Paste JSON into N8N Slack node
3. Configure N8N to pass dynamic data
4. Run workflow → Message posts with variables substituted

### Python Application
1. Use Skill to see JSON structure and get Python code example
2. Integrate with slack_sdk library
3. Use f-strings or .format() to generate JSON at runtime
4. Call client.chat_postMessage() with generated JSON

### Slack App (Bolt)
1. Use Skill to generate JSON structure
2. Integrate into your Bolt app route handlers
3. Generate JSON at runtime with your application data
4. Use app.client to post to Slack

---

## Testing Your Output

### Online Block Kit Builder (Free)
1. Copy the generated JSON
2. Visit https://api.slack.com/tools/block-kit-builder
3. Paste into "Payload" editor
4. Check preview pane for visual rendering
5. Look for green checkmark (validation passed)

### N8N Testing
1. Create test workflow with Slack node
2. Paste JSON with variables
3. Run with test data
4. Verify message appears in Slack test channel

### Python Testing
1. Use provided code example
2. Run with test data
3. Verify JSON output with json.loads()
4. Post to Slack test channel with slack_sdk

---

## Tips for Success

1. **Start simple:** Generate a basic message, then add complexity
2. **Use Block Kit Builder:** Test every JSON output before deploying
3. **Test with real data:** Use actual variable names and values
4. **Reference docs:** When unsure, check the supporting documentation
5. **Ask for examples:** Request specific use cases (approval workflows, notifications, etc.)
6. **Validate early:** Copy to Block Kit Builder immediately after generation

---

## Getting Help

### For Block Type Help
→ See [blocks-reference.md](docs/blocks-reference.md) - All 13 types documented

### For Elements & Interaction
→ See [elements-guide.md](docs/elements-guide.md) - Buttons, inputs, menus, etc.

### For Variable Substitution
→ See [variables-and-templating.md](docs/variables-and-templating.md) - N8N & Python patterns

### For Real-World Examples
→ See [examples.md](docs/examples.md) - Approval workflows, notifications, dashboards

### For Quality & Validation
→ See [best-practices.md](docs/best-practices.md) - Checklists and common mistakes

### For Surface Specifications
→ See [surfaces.md](docs/surfaces.md) - Messages, modals, home tabs limits

---

## Skill Metadata

**Surfaces Supported:** Messages (50 blocks), Modals (100 blocks), Home Tabs (100 blocks)
**Block Types:** All 13 official Slack Block Kit types
**Elements:** Buttons, select menus, date/time pickers, text inputs, radio buttons, checkboxes
**Variable Support:** N8N Jinja2, Python f-strings, Python .format()
**External Dependencies:** None (all examples embedded)
**Multi-Model:** Tested with Haiku, Sonnet, Opus
**Last Updated:** 2025-11-20

---

**Next step:** Choose a task above or ask me to generate Block Kit JSON for your specific use case.

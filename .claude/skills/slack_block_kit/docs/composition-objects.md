# Composition Objects Reference

**Building Blocks Within Blocks**

Composition objects are JSON structures used within blocks and elements to define text formatting, options lists, and confirmation dialogs.

---

## 1. Text Objects

Text objects format text for display. Used in blocks and elements throughout Block Kit.

### Plain Text Object

**Use:** Unformatted plain text (no markdown)

**Allowed in:** Most text fields

**Syntax:**
```json
{
  "type": "plain_text",
  "text": "This is plain text",
  "emoji": true
}
```

**Fields:**
- `type` (required): `"plain_text"`
- `text` (required): The text content
- `emoji` (optional): Boolean (true allows emoji like :smile:)

**When to use:**
- Button labels
- Header text
- Input labels
- Menu placeholders

---

### Markdown (mrkdwn) Text Object

**Use:** Text with markdown formatting (*bold*, _italic_, `code`)

**Allowed in:** `section` blocks, `context` blocks

**Syntax:**
```json
{
  "type": "mrkdwn",
  "text": "This is *bold* and this is _italic_ and this is `code`"
}
```

**Fields:**
- `type` (required): `"mrkdwn"`
- `text` (required): Markdown-formatted text

**Markdown syntax supported:**
- `*bold*` → Bold text
- `_italic_` → Italic text
- `~strikethrough~` → Strikethrough
- `` `code` `` → Inline code
- `[link text](https://example.com)` → Hyperlink
- `• bullet` → Bullet point (must be on new line)
- `1. ordered` → Numbered list (must be on new line)

**When to use:**
- Rich formatted content
- Emphasized text
- Links in messages
- Mixed formatting in sections

---

## 2. Option Objects

Option objects define choices for select menus, radio buttons, and checkboxes.

### Basic Option Object

**Syntax:**
```json
{
  "text": {
    "type": "plain_text",
    "text": "Option Label"
  },
  "value": "option_value"
}
```

**Fields:**
- `text` (required): Plain text label
- `value` (required): Value sent when selected
- `description` (optional): Additional text (not all elements support)
- `url` (optional): URL to open (button-specific)

---

### Option Groups

**Use:** Organize options into labeled groups (select menus only)

**Syntax:**
```json
{
  "type": "static_select",
  "option_groups": [
    {
      "label": {
        "type": "plain_text",
        "text": "Group 1"
      },
      "options": [
        {
          "text": { "type": "plain_text", "text": "Option 1" },
          "value": "option_1"
        },
        {
          "text": { "type": "plain_text", "text": "Option 2" },
          "value": "option_2"
        }
      ]
    },
    {
      "label": {
        "type": "plain_text",
        "text": "Group 2"
      },
      "options": [
        {
          "text": { "type": "plain_text", "text": "Option 3" },
          "value": "option_3"
        }
      ]
    }
  ],
  "action_id": "grouped_select_action"
}
```

**Common uses:**
- Organizing large lists
- Categorized selections
- Related options grouped together

---

## 3. Confirm Dialog Object

**Use:** Confirmation dialog for potentially destructive actions

**Syntax:**
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Delete" },
  "value": "delete",
  "action_id": "delete_action",
  "confirm": {
    "title": {
      "type": "plain_text",
      "text": "Are you sure?"
    },
    "text": {
      "type": "mrkdwn",
      "text": "This action cannot be undone."
    },
    "confirm": {
      "type": "plain_text",
      "text": "Yes, Delete"
    },
    "deny": {
      "type": "plain_text",
      "text": "Cancel"
    }
  }
}
```

**Fields:**
- `title` (required): Dialog title (plain text)
- `text` (required): Dialog body (mrkdwn or plain text)
- `confirm` (required): Confirm button text (plain text)
- `deny` (required): Cancel button text (plain text)

**When to use:**
- Delete operations
- Irreversible actions
- Critical confirmations

---

## 4. Option Object with Description

**Use:** Options with additional descriptive text (select menus)

**Syntax:**
```json
{
  "text": {
    "type": "plain_text",
    "text": "Priority: High"
  },
  "value": "high",
  "description": {
    "type": "plain_text",
    "text": "Urgent, needs immediate attention"
  }
}
```

**Note:** Not all elements support descriptions. Check element documentation.

---

## 5. Block Object Variations

### Fields Array in Section Blocks

**Use:** Display multiple columns of text in a section

**Syntax:**
```json
{
  "type": "section",
  "fields": [
    {
      "type": "mrkdwn",
      "text": "*Author:*\nJohn Doe"
    },
    {
      "type": "mrkdwn",
      "text": "*Date:*\nNov 20, 2025"
    },
    {
      "type": "mrkdwn",
      "text": "*Priority:*\nHigh"
    },
    {
      "type": "mrkdwn",
      "text": "*Status:*\nIn Progress"
    }
  ]
}
```

**Rules:**
- Maximum 10 fields per section
- Alternates between 2 columns (1 field = 1 col, 2 fields = 1 col each, 3 fields = 2 cols + 1 col, 4+ = 2 cols each)
- Each field is a text object (plain_text or mrkdwn)

---

## Common Composition Patterns

### Formatted Text with Emphasis

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Important:* Please _review_ and `approve` this request.\n\nVisit <https://example.com|review page> for details."
  }
}
```

### Select Menu with Option Groups

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "static_select",
      "placeholder": { "type": "plain_text", "text": "Select priority" },
      "option_groups": [
        {
          "label": { "type": "plain_text", "text": "Urgent" },
          "options": [
            { "text": { "type": "plain_text", "text": "Critical" }, "value": "critical" }
          ]
        },
        {
          "label": { "type": "plain_text", "text": "Normal" },
          "options": [
            { "text": { "type": "plain_text", "text": "High" }, "value": "high" },
            { "text": { "type": "plain_text", "text": "Medium" }, "value": "medium" },
            { "text": { "type": "plain_text", "text": "Low" }, "value": "low" }
          ]
        }
      ],
      "action_id": "priority_select"
    }
  ]
}
```

### Delete Button with Confirmation

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Delete Task" },
      "value": "delete_task",
      "action_id": "delete_action",
      "style": "danger",
      "confirm": {
        "title": { "type": "plain_text", "text": "Delete Task?" },
        "text": { "type": "mrkdwn", "text": "This cannot be undone. Are you sure?" },
        "confirm": { "type": "plain_text", "text": "Delete" },
        "deny": { "type": "plain_text", "text": "Cancel" }
      }
    }
  ]
}
```

### Multi-Column Information Section

```json
{
  "type": "section",
  "fields": [
    { "type": "mrkdwn", "text": "*Status:*\nApproved" },
    { "type": "mrkdwn", "text": "*Last Updated:*\n2 hours ago" },
    { "type": "mrkdwn", "text": "*Assigned To:*\nAlice Smith" },
    { "type": "mrkdwn", "text": "*Priority:*\nHigh" }
  ]
}
```

---

## Text Formatting Quick Reference

| Format | Syntax | Example |
|--------|--------|---------|
| Bold | `*text*` | `*bold*` |
| Italic | `_text_` | `_italic_` |
| Strikethrough | `~text~` | `~strike~` |
| Code | `` `text` `` | `` `code` `` |
| Link | `[text](url)` | `[link](https://example.com)` |
| Bullet | `• text` | `• item` |
| List | `1. text` | `1. first` |
| Emoji | `:emoji_name:` | `:smile:` |

---

## Important Notes

### Text Object Context
- Use `plain_text` when formatting not needed (button labels, headers)
- Use `mrkdwn` when you need emphasis, links, or formatting (section bodies, context text)
- Not all fields accept both types; check specific block/element documentation

### Option Lists
- Keep option labels short and clear
- Group related options with `option_groups`
- Use `value` for backend/form data, not for display
- Descriptions are only supported in some elements

### Confirmations
- Use for delete/cancel operations
- Keep title and text clear and concise
- Confirm/deny button text should be specific action descriptions

---

**Next:** See [blocks-reference.md](blocks-reference.md) to understand which blocks contain these composition objects, or [surfaces.md](surfaces.md) for surface-specific limitations.

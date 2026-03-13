# Surfaces Specification

**Three Slack Surfaces: Messages, Modals, Home Tabs**

Each surface has different limitations, purposes, and allowed block types.

---

## 1. Messages (Messaging)

**Purpose:** Post messages to channels and direct messages

**Access:** Sent via chat.postMessage, webhooks, or app responses

**Block Limit:** Maximum 50 blocks per message

**Surfaces Features:**
- Display-focused
- One-way communication
- User-triggered actions via buttons
- No form submission (except modals)

### Message Payload Structure

**Syntax:**
```json
{
  "text": "Fallback text for notifications and accessibility",
  "blocks": [
    { "type": "section", "text": { "type": "mrkdwn", "text": "Message content" } }
  ],
  "thread_ts": "1234567890.123456"
}
```

**Top-level fields:**
- `text` (required): Fallback text (shown in notifications, required for accessibility)
- `blocks` (optional): Array of blocks (max 50)
- `thread_ts` (optional): Reply in thread
- `reply_broadcast` (optional): Share thread reply to channel
- `metadata` (optional): Message metadata

### Allowed Block Types in Messages

**All 13 block types can appear in messages EXCEPT:**
- `input` block (modals only)

**Surface-specific blocks:**
- `markdown` block (messages only)
- `context_actions` block (messages only)

### Common Message Patterns

#### Notification Message
```json
{
  "text": "New task assigned",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "New Task Assignment" }
    },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Task:* Quarterly Review\n*Assigned to:* @alice\n*Due:* Tomorrow" }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "View Task" },
          "url": "https://example.com/task/123"
        }
      ]
    }
  ]
}
```

#### Approval Request
```json
{
  "text": "Budget approval needed",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Budget Approval Request*\n\nAmount: $5,000\nRequester: John Doe\nReason: Q4 Marketing Campaign"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Approve" },
          "value": "approve",
          "action_id": "approve_action",
          "style": "primary"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Deny" },
          "value": "deny",
          "action_id": "deny_action",
          "style": "danger"
        }
      ]
    }
  ]
}
```

#### Alert with Divider
```json
{
  "text": "System maintenance alert",
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": "System Maintenance" } },
    { "type": "section", "text": { "type": "mrkdwn", "text": "Scheduled maintenance tonight from 10 PM - 2 AM." } },
    { "type": "divider" },
    { "type": "context", "elements": [ { "type": "plain_text", "text": "Updates will be posted in #status-updates" } ] }
  ]
}
```

### Message Block Limits & Tips

**Block limit:** 50 blocks

**Tips for staying under limit:**
- Combine text into single `section` blocks
- Use `fields` array in sections for columns
- Use `divider` blocks sparingly
- Condense layout before hitting limit

---

## 2. Modals

**Purpose:** Collect user input through forms

**Access:** Opened via button click, shortcut, or slash command

**Block Limit:** Maximum 100 blocks per modal

**Modal Features:**
- Form-focused
- Input blocks for collecting data
- Submit/Close buttons
- Single-step workflows (v1)
- Modal callbacks and submissions

### Modal Payload Structure

**Syntax:**
```json
{
  "type": "modal",
  "callback_id": "view_callback",
  "title": {
    "type": "plain_text",
    "text": "Modal Title"
  },
  "submit": {
    "type": "plain_text",
    "text": "Submit"
  },
  "close": {
    "type": "plain_text",
    "text": "Cancel"
  },
  "blocks": [
    { "type": "input", "block_id": "input_1", "label": { "type": "plain_text", "text": "Field" }, "element": { "type": "plain_text_input", "action_id": "input_action" } }
  ]
}
```

**Top-level fields:**
- `type` (required): `"modal"`
- `callback_id` (required): Unique ID for form submission handling
- `title` (required): Modal title (plain text)
- `submit` (required): Submit button text
- `close` (required): Close/cancel button text
- `blocks` (required): Array of blocks (max 100)
- `private_metadata` (optional): Hidden data passed with submission
- `notify_on_close` (optional): Notify app when closed

### Allowed Block Types in Modals

**All 13 block types can appear in modals EXCEPT:**
- `markdown` block (messages only)
- `context_actions` block (messages only)

**Surface-specific blocks:**
- `input` block (modals only)

### Form Input Patterns

**Text Input:**
```json
{
  "type": "input",
  "block_id": "username_block",
  "label": { "type": "plain_text", "text": "Username" },
  "element": {
    "type": "plain_text_input",
    "action_id": "username_input",
    "placeholder": { "type": "plain_text", "text": "Enter username" }
  },
  "optional": false
}
```

**Text Area:**
```json
{
  "type": "input",
  "block_id": "feedback_block",
  "label": { "type": "plain_text", "text": "Feedback" },
  "element": {
    "type": "plain_text_input",
    "action_id": "feedback_input",
    "multiline": true
  }
}
```

**Select Dropdown:**
```json
{
  "type": "input",
  "block_id": "priority_block",
  "label": { "type": "plain_text", "text": "Priority" },
  "element": {
    "type": "static_select",
    "action_id": "priority_select",
    "options": [
      { "text": { "type": "plain_text", "text": "Low" }, "value": "low" },
      { "text": { "type": "plain_text", "text": "Medium" }, "value": "medium" },
      { "text": { "type": "plain_text", "text": "High" }, "value": "high" }
    ]
  }
}
```

**Date Picker:**
```json
{
  "type": "input",
  "block_id": "date_block",
  "label": { "type": "plain_text", "text": "Due Date" },
  "element": {
    "type": "datepicker",
    "action_id": "date_picker"
  }
}
```

**Checkboxes:**
```json
{
  "type": "input",
  "block_id": "features_block",
  "label": { "type": "plain_text", "text": "Select features:" },
  "element": {
    "type": "checkboxes",
    "action_id": "features_checkbox",
    "options": [
      { "text": { "type": "plain_text", "text": "Feature A" }, "value": "feature_a" },
      { "text": { "type": "plain_text", "text": "Feature B" }, "value": "feature_b" }
    ]
  }
}
```

### Common Modal Patterns

#### Simple Feedback Form
```json
{
  "type": "modal",
  "callback_id": "feedback_modal",
  "title": { "type": "plain_text", "text": "Send Feedback" },
  "submit": { "type": "plain_text", "text": "Send" },
  "close": { "type": "plain_text", "text": "Cancel" },
  "blocks": [
    {
      "type": "input",
      "block_id": "feedback_input",
      "label": { "type": "plain_text", "text": "Your Feedback" },
      "element": {
        "type": "plain_text_input",
        "action_id": "feedback_action",
        "multiline": true,
        "placeholder": { "type": "plain_text", "text": "Tell us what you think..." }
      }
    },
    {
      "type": "input",
      "block_id": "email_input",
      "label": { "type": "plain_text", "text": "Email (optional)" },
      "element": {
        "type": "plain_text_input",
        "action_id": "email_action"
      },
      "optional": true
    }
  ]
}
```

#### Bug Report Modal
```json
{
  "type": "modal",
  "callback_id": "bug_report_modal",
  "title": { "type": "plain_text", "text": "Report Bug" },
  "submit": { "type": "plain_text", "text": "Submit Report" },
  "close": { "type": "plain_text", "text": "Cancel" },
  "blocks": [
    {
      "type": "input",
      "block_id": "title_input",
      "label": { "type": "plain_text", "text": "Bug Title" },
      "element": { "type": "plain_text_input", "action_id": "title_action" }
    },
    {
      "type": "input",
      "block_id": "description_input",
      "label": { "type": "plain_text", "text": "Description" },
      "element": { "type": "plain_text_input", "action_id": "description_action", "multiline": true }
    },
    {
      "type": "input",
      "block_id": "severity_input",
      "label": { "type": "plain_text", "text": "Severity" },
      "element": {
        "type": "static_select",
        "action_id": "severity_action",
        "options": [
          { "text": { "type": "plain_text", "text": "Low" }, "value": "low" },
          { "text": { "type": "plain_text", "text": "Medium" }, "value": "medium" },
          { "text": { "type": "plain_text", "text": "Critical" }, "value": "critical" }
        ]
      }
    }
  ]
}
```

### Modal Limitations (v1)

- **Single-step only:** No `previous_view_id` (multi-step deferred to v2)
- **Block limit:** 100 blocks maximum
- **Form submission:** Handled by app backend (Skill generates JSON structure only)

---

## 3. Home Tab

**Purpose:** Persistent personalized dashboard interface

**Access:** Always visible in Slack app sidebar

**Block Limit:** Maximum 100 blocks per home tab

**Home Tab Features:**
- Persistent interface (always visible)
- Personalized per user
- Dashboard/overview layout
- Updates reflected in real-time
- Non-linear navigation

### Home Tab Payload Structure

**Syntax:**
```json
{
  "type": "home",
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": "Welcome" } },
    { "type": "section", "text": { "type": "mrkdwn", "text": "Dashboard content" } }
  ]
}
```

**Top-level fields:**
- `type` (required): `"home"`
- `blocks` (required): Array of blocks (max 100)
- `private_metadata` (optional): Hidden data

### Allowed Block Types in Home Tab

**All 13 block types can appear in home tabs EXCEPT:**
- `markdown` block (messages only)
- `context_actions` block (messages only)

### Common Home Tab Patterns

#### Welcome Dashboard
```json
{
  "type": "home",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "Welcome, Alice! 👋" }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Your Tasks (3)*" }
    },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "1. Complete Q4 Report\n2. Review Team Proposal\n3. Attend Meeting at 2 PM" }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Quick Actions*" },
      "accessory": {
        "type": "button",
        "text": { "type": "plain_text", "text": "View All Tasks" },
        "url": "https://example.com/tasks"
      }
    }
  ]
}
```

#### User Profile Home Tab
```json
{
  "type": "home",
  "blocks": [
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Profile: Alice Smith*" },
      "accessory": {
        "type": "image",
        "image_url": "https://example.com/profile.jpg",
        "alt_text": "Profile picture"
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Team:*\nEngineering" },
        { "type": "mrkdwn", "text": "*Role:*\nSenior Engineer" },
        { "type": "mrkdwn", "text": "*Joined:*\nJan 2020" },
        { "type": "mrkdwn", "text": "*Status:*\n🟢 Available" }
      ]
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Recent Activity*" }
    },
    {
      "type": "context",
      "elements": [ { "type": "plain_text", "text": "Last updated 5 minutes ago" } ]
    }
  ]
}
```

---

## Surface Comparison

| Feature | Messages | Modals | Home Tabs |
|---------|----------|--------|-----------|
| **Block Limit** | 50 | 100 | 100 |
| **Primary Use** | Notifications | Forms | Dashboards |
| **Input Fields** | No | Yes | No |
| **User-Triggered** | Button clicks | Form submit | Always visible |
| **Persistence** | Temporary | Modal lifetime | Persistent |
| **markdown block** | ✓ | ✗ | ✗ |
| **input block** | ✗ | ✓ | ✗ |
| **context_actions** | ✓ | ✗ | ✗ |

---

## Surface Selection Checklist

### Use Messages When:
- [ ] Sending notifications or alerts
- [ ] Requesting approval/action
- [ ] Sharing information
- [ ] Simple interactive options needed
- [ ] No form submission required

### Use Modals When:
- [ ] Collecting user input
- [ ] Creating/editing forms
- [ ] Multi-field data entry
- [ ] Modal workflow expected
- [ ] Form submission needed

### Use Home Tabs When:
- [ ] Persistent dashboard needed
- [ ] Personalized interface required
- [ ] Overview/summary display
- [ ] Always-accessible interface
- [ ] No immediate action needed

---

**Next:** See [variables-and-templating.md](variables-and-templating.md) for variable substitution patterns across surfaces, or [examples.md](examples.md) for complete surface-specific use cases.

# Interactive Elements Guide

**Block Kit Elements: Interactive Components**

Elements are interactive components that live *inside* blocks. They are NOT separate block types.

---

## Element Containment Rules

**Where elements can appear:**
- `section` block → `accessory` field (single element)
- `actions` block → `elements` array (multiple elements)
- `input` block → `element` field (single element)

**Elements cannot be used:**
- As top-level blocks
- In messages without a container block
- Outside of their allowed surfaces

---

## Element Types

### 1. Button Element

**Use:** Clickable button with action

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "button",
  "text": {
    "type": "plain_text",
    "text": "Click Me"
  },
  "value": "click_me_123",
  "action_id": "button_action"
}
```

**Fields:**
- `type` (required): `"button"`
- `text` (required): Plain text label
- `value` (required): Value sent when clicked
- `action_id` (required): Unique identifier for event handling
- `url` (optional): URL to open when clicked (instead of action_id)
- `style` (optional): `"primary"` (blue) or `"danger"` (red)
- `confirm` (optional): Confirmation dialog before action

**Examples:**
- Approval buttons (Approve/Deny)
- Link buttons (Learn More)
- Action buttons (Complete, Archive, Delete)
- Primary/danger style buttons

---

### 2. Static Select Menu

**Use:** Dropdown menu with predefined options

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "static_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select an option"
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
  ],
  "action_id": "select_action"
}
```

**Fields:**
- `type` (required): `"static_select"`
- `placeholder` (optional): Placeholder text
- `options` (required): Array of option objects
- `action_id` (required): Unique identifier
- `initial_option` (optional): Pre-selected option

**Common Uses:**
- Dropdown menus
- Priority selection (Low/Medium/High)
- Category selection
- Status selection

---

### 3. External Select Menu

**Use:** Dropdown that loads options from external data source

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "external_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Search..."
  },
  "action_id": "external_select_action"
}
```

**Note:** External select requires backend implementation to handle dynamic option loading. Used primarily in modals and home tabs where user interactions are expected.

---

### 4. User Select Menu

**Use:** Dropdown for selecting Slack users

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "users_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select a user"
  },
  "action_id": "user_select_action"
}
```

**Fields:**
- `type` (required): `"users_select"`
- `placeholder` (optional): Placeholder text
- `action_id` (required): Unique identifier
- `initial_user` (optional): Pre-selected user ID

---

### 5. Conversation Select Menu

**Use:** Dropdown for selecting Slack channels/conversations

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "conversations_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select a channel"
  },
  "action_id": "channel_select_action"
}
```

---

### 6. Date Picker Element

**Use:** Calendar picker for selecting dates

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "datepicker",
  "action_id": "date_select_action",
  "placeholder": {
    "type": "plain_text",
    "text": "Select date"
  }
}
```

**Fields:**
- `type` (required): `"datepicker"`
- `action_id` (required): Unique identifier
- `placeholder` (optional): Placeholder text
- `initial_date` (optional): Pre-selected date (YYYY-MM-DD)

---

### 7. Time Picker Element

**Use:** Clock picker for selecting times

**Container Blocks:** `section` (accessory), `actions` (elements), `input` (element)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "timepicker",
  "action_id": "time_select_action",
  "placeholder": {
    "type": "plain_text",
    "text": "Select time"
  }
}
```

**Fields:**
- `type` (required): `"timepicker"`
- `action_id` (required): Unique identifier
- `placeholder` (optional): Placeholder text
- `initial_time` (optional): Pre-selected time (HH:MM)

---

### 8. Plain Text Input Element

**Use:** Single or multi-line text input field

**Container Blocks:** `input` block only

**Surfaces:** Modals (mainly), some in messages via actions

**Syntax:**
```json
{
  "type": "plain_text_input",
  "action_id": "text_input_action",
  "placeholder": {
    "type": "plain_text",
    "text": "Enter text..."
  },
  "multiline": false
}
```

**Fields:**
- `type` (required): `"plain_text_input"`
- `action_id` (required): Unique identifier
- `placeholder` (optional): Placeholder text
- `multiline` (optional): Boolean (true for textarea)
- `initial_value` (optional): Pre-filled text

**Common Uses:**
- Text fields
- Text areas
- Feedback forms
- Name/email inputs

---

### 9. Radio Button Group

**Use:** Mutually exclusive selection options

**Container Blocks:** `input` block

**Surfaces:** Modals, Home Tabs

**Syntax:**
```json
{
  "type": "radio_buttons",
  "options": [
    {
      "text": { "type": "plain_text", "text": "Option 1" },
      "value": "option_1"
    },
    {
      "text": { "type": "plain_text", "text": "Option 2" },
      "value": "option_2"
    }
  ],
  "action_id": "radio_action"
}
```

**Fields:**
- `type` (required): `"radio_buttons"`
- `options` (required): Array of option objects
- `action_id` (required): Unique identifier
- `initial_option` (optional): Pre-selected option

---

### 10. Checkbox Group

**Use:** Multiple selection options (check/uncheck)

**Container Blocks:** `input` block

**Surfaces:** Modals, Home Tabs

**Syntax:**
```json
{
  "type": "checkboxes",
  "options": [
    {
      "text": { "type": "plain_text", "text": "Option 1" },
      "value": "option_1"
    },
    {
      "text": { "type": "plain_text", "text": "Option 2" },
      "value": "option_2"
    }
  ],
  "action_id": "checkbox_action"
}
```

**Fields:**
- `type` (required): `"checkboxes"`
- `options` (required): Array of option objects
- `action_id` (required): Unique identifier
- `initial_options` (optional): Array of pre-checked options

---

## Element Placement Quick Reference

### In `section` block (single accessory)
```json
{
  "type": "section",
  "text": { "type": "mrkdwn", "text": "Text here" },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "Button" },
    "action_id": "button_action"
  }
}
```

### In `actions` block (multiple elements)
```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Approve" },
      "action_id": "approve_action"
    },
    {
      "type": "static_select",
      "options": [...],
      "action_id": "select_action"
    }
  ]
}
```

### In `input` block (form field)
```json
{
  "type": "input",
  "block_id": "input_block",
  "label": { "type": "plain_text", "text": "Choose option:" },
  "element": {
    "type": "static_select",
    "options": [...],
    "action_id": "select_action"
  }
}
```

---

## Element Type Quick Reference

| Element | Container | Surfaces | Purpose |
|---------|-----------|----------|---------|
| button | section, actions | All | Clickable action |
| static_select | section, actions, input | All | Dropdown menu |
| external_select | section, actions, input | All | Dynamic dropdown |
| users_select | section, actions, input | All | User picker |
| conversations_select | section, actions, input | All | Channel picker |
| datepicker | section, actions, input | All | Date picker |
| timepicker | section, actions, input | All | Time picker |
| plain_text_input | input | Modals | Text input/textarea |
| radio_buttons | input | Modals, Home Tabs | Radio options |
| checkboxes | input | Modals, Home Tabs | Multi-select |

---

## Common Element Patterns

### Approval Buttons
```json
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
```

### Form with Multiple Inputs
```json
{
  "type": "input",
  "block_id": "name_input",
  "label": { "type": "plain_text", "text": "Full Name" },
  "element": {
    "type": "plain_text_input",
    "action_id": "name_action"
  }
},
{
  "type": "input",
  "block_id": "priority_input",
  "label": { "type": "plain_text", "text": "Priority" },
  "element": {
    "type": "static_select",
    "options": [
      { "text": { "type": "plain_text", "text": "Low" }, "value": "low" },
      { "text": { "type": "plain_text", "text": "High" }, "value": "high" }
    ],
    "action_id": "priority_action"
  }
}
```

### Section with Button Accessory
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Task:* Complete report\n*Due:* Tomorrow"
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "Complete" },
    "action_id": "complete_action",
    "style": "primary"
  }
}
```

---

**Important:** Remember that elements must live inside container blocks. They cannot stand alone in JSON. Always check [blocks-reference.md](blocks-reference.md) for which blocks accept which elements.

**Next:** See [composition-objects.md](composition-objects.md) for text objects and option lists, or [surfaces.md](surfaces.md) for surface-specific element support.

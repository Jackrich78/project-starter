# Block Types Reference

**13 Official Slack Block Kit Block Types**

All block types documented with syntax, required fields, and when to use.

---

## 1. Section Block

**Use:** Display text with optional accessory element (most versatile block)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Text with *bold* and _italic_"
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "Click Me" },
    "value": "click_me_123"
  }
}
```

**Fields:**
- `type` (required): `"section"`
- `text` (optional): Text object (mrkdwn or plain_text)
- `accessory` (optional): Single element (button, select, date picker, etc.)
- `block_id` (optional): Unique identifier for form data
- `fields` (optional): Array of text objects (up to 10) for columns

**Common Patterns:**
- Simple text section
- Text with button/link
- Text with image accessory
- Multi-column text layout using `fields` array

---

## 2. Header Block

**Use:** Large-sized text header for visual section breaks

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "header",
  "text": {
    "type": "plain_text",
    "text": "Section Title"
  }
}
```

**Fields:**
- `type` (required): `"header"`
- `text` (required): Plain text only (no markdown)
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Section heading
- Modal title alternative
- Visual separator with text

---

## 3. Image Block

**Use:** Display images with alt text

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "image",
  "image_url": "https://example.com/image.png",
  "alt_text": "Description for accessibility"
}
```

**Fields:**
- `type` (required): `"image"`
- `image_url` (required): HTTPS URL to image
- `alt_text` (required): Accessibility description
- `title` (optional): Caption above image
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Product or screenshot display
- Icon/avatar display
- Image gallery layouts

---

## 4. Video Block

**Use:** Embed video players

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "video",
  "video_url": "https://example.com/video.mp4",
  "thumbnail_url": "https://example.com/thumbnail.png",
  "alt_text": "Video description"
}
```

**Fields:**
- `type` (required): `"video"`
- `video_url` (required): HTTPS URL to video file
- `thumbnail_url` (required): HTTPS URL to thumbnail image
- `alt_text` (required): Accessibility description
- `title` (optional): Video title/caption
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Tutorial video embedding
- Demo video display
- Instructional content

---

## 5. Markdown Block

**Use:** Text with markdown formatting (messages only)

**Surfaces:** Messages ONLY (not modals or home tabs)

**Syntax:**
```json
{
  "type": "markdown",
  "text": "# Heading\n\nBody text with *emphasis*"
}
```

**Fields:**
- `type` (required): `"markdown"`
- `text` (required): Markdown-formatted text
- `block_id` (optional): Unique identifier

**Note:** This block only works in messages. For modals/home tabs, use `section` blocks with mrkdwn text objects instead.

**Common Patterns:**
- Message bodies with rich formatting
- Headers and subheaders
- Lists and emphasis

---

## 6. Rich Text Block

**Use:** Structured text with rich formatting (bold, italic, code, links, lists)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        {
          "type": "text",
          "text": "Bold text: "
        },
        {
          "type": "text",
          "text": "emphasized",
          "style": { "bold": true }
        }
      ]
    }
  ]
}
```

**Fields:**
- `type` (required): `"rich_text"`
- `elements` (required): Array of rich_text_section elements
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Structured document formatting
- Lists with bullets/numbers
- Code blocks
- Multi-paragraph formatted text

---

## 7. Divider Block

**Use:** Visual separator line

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "divider"
}
```

**Fields:**
- `type` (required): `"divider"`
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Section separation
- Visual spacing
- Grouping related content

---

## 8. Context Block

**Use:** Small text with optional images (supplementary information)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "context",
  "elements": [
    {
      "type": "plain_text",
      "text": "Posted by user • 2 hours ago"
    }
  ]
}
```

**Fields:**
- `type` (required): `"context"`
- `elements` (required): Array of text or image elements (max 10)
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Metadata (timestamps, authors)
- User information
- Small supplementary text
- Image + text combos

---

## 9. File Block

**Use:** Display remote file information (metadata, preview)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "file",
  "external_id": "file_123",
  "source": "remote"
}
```

**Fields:**
- `type` (required): `"file"`
- `external_id` (required): File ID from Slack File API
- `source` (required): `"remote"` (for remote files)
- `block_id` (optional): Unique identifier

**Common Patterns:**
- File sharing/display
- Document metadata
- File preview

---

## 10. Table Block

**Use:** Structured tabular data display

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
{
  "type": "table",
  "border": 1,
  "elements": [
    [
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              { "type": "text", "text": "Header 1" }
            ]
          }
        ]
      },
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              { "type": "text", "text": "Header 2" }
            ]
          }
        ]
      }
    ],
    [
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              { "type": "text", "text": "Data 1" }
            ]
          }
        ]
      },
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              { "type": "text", "text": "Data 2" }
            ]
          }
        ]
      }
    ]
  ]
}
```

**Fields:**
- `type` (required): `"table"`
- `elements` (required): 2D array of rich_text blocks (rows × columns)
- `border` (optional): 1 (with border) or 0 (no border)
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Sales/analytics data
- Schedule/timeline
- Comparison tables
- Structured reports

---

## 11. Actions Block

**Use:** Container for interactive elements (buttons, selects, date pickers)

**Surfaces:** Messages, Modals, Home Tabs

**Syntax:**
```json
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
```

**Fields:**
- `type` (required): `"actions"`
- `elements` (required): Array of element objects (buttons, selects, date pickers, etc.)
- `block_id` (optional): Unique identifier

**Common Patterns:**
- Button groups
- Action menus
- Form control sections
- Multi-step workflows

---

## 12. Input Block

**Use:** Form input fields (modals only)

**Surfaces:** Modals ONLY (not messages or home tabs)

**Syntax:**
```json
{
  "type": "input",
  "block_id": "username_input",
  "label": {
    "type": "plain_text",
    "text": "Username"
  },
  "element": {
    "type": "plain_text_input",
    "action_id": "username_action"
  },
  "optional": false
}
```

**Fields:**
- `type` (required): `"input"`
- `block_id` (required): Unique identifier for form submission
- `label` (required): Plain text label
- `element` (required): Input element (text, select, date picker, etc.)
- `optional` (optional): Boolean (default: false)
- `dispatch_action` (optional): Boolean (submit on change)

**Common Patterns:**
- Text input fields
- Select dropdowns
- Date/time pickers
- Checkboxes/radio groups
- Multi-line text areas

---

## 13. Context Actions Block

**Use:** Actions displayed as contextual info in messages (not traditional buttons)

**Surfaces:** Messages ONLY (not modals or home tabs)

**Syntax:**
```json
{
  "type": "context_actions",
  "actions": [
    {
      "type": "action",
      "url": "https://example.com/action"
    }
  ]
}
```

**Fields:**
- `type` (required): `"context_actions"`
- `actions` (required): Array of action objects (URLs/links)

**Common Patterns:**
- Message metadata actions
- Linked actions in context
- Quick access links

---

## Block Type Quick Reference

| Block | Surface | Purpose | Key Feature |
|-------|---------|---------|-------------|
| section | All | Text + element | Most versatile |
| header | All | Large title | Visual emphasis |
| image | All | Image display | Alt text required |
| video | All | Video embed | Thumbnail + URL |
| markdown | Messages | Rich text | Messages only |
| rich_text | All | Structured formatting | Lists, code blocks |
| divider | All | Visual separator | Simple spacer |
| context | All | Small metadata | Images + text |
| file | All | File display | Remote files |
| table | All | Tabular data | Row/column grid |
| actions | All | Interactive elements | Buttons, menus |
| input | Modals | Form inputs | Modals only |
| context_actions | Messages | Message actions | Messages only |

---

## When to Use Which Block

### For Text Display
- **Simple text + optional button?** → `section` block
- **Large heading?** → `header` block
- **Rich formatted text?** → `rich_text` block
- **Simple paragraph?** → `section` block with text

### For Media
- **Images?** → `image` block
- **Videos?** → `video` block

### For Structure
- **Section break?** → `divider` block
- **Small metadata text?** → `context` block
- **Tabular data?** → `table` block
- **File information?** → `file` block

### For Interaction
- **Buttons/menus in message?** → `actions` block
- **Form inputs in modal?** → `input` block
- **Context actions?** → `context_actions` block (messages only)

---

**Next:** See [elements-guide.md](elements-guide.md) for interactive element types, or [surfaces.md](surfaces.md) for surface-specific limitations.

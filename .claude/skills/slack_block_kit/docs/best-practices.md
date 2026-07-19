# Best Practices & Validation

**Quality Assurance, Accessibility, and Common Mistakes**

---

## JSON Validation Checklist

Use this checklist before deploying Block Kit JSON:

### Syntax Validation
- [ ] Valid JSON (no missing commas, quotes, or brackets)
- [ ] All field names are quoted strings
- [ ] All string values are quoted
- [ ] Arrays use square brackets `[]`
- [ ] Objects use curly braces `{}`

### Block Kit Validation
- [ ] Pasted into Block Kit Builder with green checkmark
- [ ] Visual rendering matches intent
- [ ] No validation errors or warnings

### Surface Validation
- [ ] Blocks appropriate for surface (message/modal/home tab)
- [ ] Block count under limit (50 for messages, 100 for modals/home tabs)
- [ ] Input blocks only in modals (not messages/home tabs)
- [ ] markdown blocks only in messages (not modals/home tabs)

### Field Validation
- [ ] All required fields present
- [ ] Text fields not empty
- [ ] block_id values unique (if present)
- [ ] action_id values unique (if present)
- [ ] URLs valid and complete (https://)

### Element Validation
- [ ] Elements in correct container blocks
- [ ] Buttons have text and action_id or url
- [ ] Select menus have options
- [ ] Input blocks have element field
- [ ] All interactive elements have action_id

---

## Common Mistakes & How to Fix Them

### Mistake 1: Missing Required Fields

**Problem:** Block Kit Builder shows red X

**Example:**
```json
{
  "type": "section"
  // Missing: text field (required)
}
```

**Fix:**
```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Content here"
  }
}
```

### Mistake 2: Input Blocks in Messages

**Problem:** Input blocks are modal-only

**Wrong:**
```json
{
  "text": "Message",
  "blocks": [
    {
      "type": "input",  // ❌ Not allowed in messages
      "block_id": "input",
      "label": { "type": "plain_text", "text": "Field" },
      "element": { "type": "plain_text_input", "action_id": "input" }
    }
  ]
}
```

**Fix:** Use modal or use buttons/actions blocks in message instead:
```json
{
  "text": "Request",
  "blocks": [
    {
      "type": "actions",  // ✓ Correct for messages
      "elements": [
        { "type": "button", "text": { "type": "plain_text", "text": "Approve" }, "action_id": "approve" }
      ]
    }
  ]
}
```

### Mistake 3: Markdown in Plain Text

**Problem:** Formatting doesn't work in plain_text type

**Wrong:**
```json
{
  "type": "plain_text",
  "text": "*bold* and _italic_"  // ❌ Won't format
}
```

**Fix:** Use `mrkdwn` type instead:
```json
{
  "type": "mrkdwn",
  "text": "*bold* and _italic_"  // ✓ Will format
}
```

### Mistake 4: Buttons Without action_id or url

**Problem:** Button doesn't trigger action

**Wrong:**
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click" }
  // Missing: action_id or url
}
```

**Fix:**
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click" },
  "action_id": "button_action"  // ✓ For app to handle
  // OR
  "url": "https://example.com"  // ✓ For direct link
}
```

### Mistake 5: Duplicate block_id or action_id

**Problem:** Form submission data ambiguous

**Wrong:**
```json
{
  "type": "input",
  "block_id": "input_1",
  "label": { "type": "plain_text", "text": "Name" },
  "element": { "type": "plain_text_input", "action_id": "input_1" }
},
{
  "type": "input",
  "block_id": "input_1",  // ❌ Duplicate!
  "label": { "type": "plain_text", "text": "Email" },
  "element": { "type": "plain_text_input", "action_id": "input_1" }  // ❌ Duplicate!
}
```

**Fix:** Make IDs unique:
```json
{
  "type": "input",
  "block_id": "name_input",  // ✓ Unique
  "label": { "type": "plain_text", "text": "Name" },
  "element": { "type": "plain_text_input", "action_id": "name_action" }  // ✓ Unique
},
{
  "type": "input",
  "block_id": "email_input",  // ✓ Unique
  "label": { "type": "plain_text", "text": "Email" },
  "element": { "type": "plain_text_input", "action_id": "email_action" }  // ✓ Unique
}
```

### Mistake 6: Exceeding Block Limits

**Problem:** Message has 75 blocks (limit is 50)

**Symptoms:** Block Kit Builder warning or message fails to post

**Fix:**
- Combine text into fewer blocks
- Use `fields` array in sections for columns
- Remove decorative dividers
- Test block count: Count all `"type": "..."` entries

**Block Count Formula:**
```
total_blocks = count of all "type" fields at block level (not inside elements)
```

### Mistake 7: Invalid URLs

**Problem:** Button or link has broken URL

**Wrong:**
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click" },
  "url": "example.com/page"  // ❌ Missing https://
}
```

**Fix:**
```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click" },
  "url": "https://example.com/page"  // ✓ Complete URL
}
```

### Mistake 8: Elements Outside Containers

**Problem:** Elements (buttons, inputs) not in allowed container blocks

**Wrong:**
```json
{
  "blocks": [
    {
      "type": "button",  // ❌ Not a valid block type (it's an element)
      "text": { "type": "plain_text", "text": "Click" },
      "action_id": "button"
    }
  ]
}
```

**Fix:** Put elements in container blocks:
```json
{
  "blocks": [
    {
      "type": "actions",  // ✓ Valid container
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Click" },
          "action_id": "button"
        }
      ]
    }
  ]
}
```

---

## Accessibility Guidelines

### Text Descriptions
- [ ] Alt text for all images (`alt_text` field)
- [ ] Descriptive button labels (not just "Click")
- [ ] Context for visual-only information
- [ ] Form labels for all input fields

### Color & Contrast
- [ ] Don't rely on color alone to convey information
- [ ] Use text labels alongside color indicators
- [ ] Sufficient contrast between text and background

### Example:
```json
{
  "type": "section",
  "fields": [
    {
      "type": "mrkdwn",
      "text": "*Status: In Progress*\n🟡 Waiting for approval"  // Text + emoji, not color alone
    }
  ]
}
```

### Keyboard Navigation
- [ ] All interactive elements reachable by Tab key
- [ ] Buttons activatable with Enter/Space
- [ ] Modals closable with Escape
- [ ] Logical tab order

---

## Performance Tips

### Keep Messages Lightweight
1. **Block count:** Stay well below limits (target <30 for messages)
2. **Text length:** Prefer concise text over paragraphs
3. **Image optimization:** Use compressed images
4. **External requests:** Minimize external data fetching

### Optimize Modal Load Time
1. **Block count:** Use <50 blocks if possible (limit is 100)
2. **Lazy load:** Load additional data on user interaction
3. **Cache:** Cache options for select menus when possible

### Efficient Variable Substitution
1. **N8N:** Fetch only needed data from previous nodes
2. **Python:** Pre-process data before generating JSON
3. **Caching:** Reuse JSON templates, vary only data

---

## Testing Strategy

### Level 1: Syntax Validation
```
1. Generate JSON
2. Paste into Block Kit Builder
3. Check for green checkmark
4. No errors or warnings
```

### Level 2: Visual Validation
```
1. Check preview pane
2. Verify layout matches intent
3. Check text readability
4. Verify all elements visible
```

### Level 3: Functional Testing
- **N8N:** Run workflow with test data, verify substitution
- **Python:** Run code with test data, verify JSON output
- **Slack:** Post to test channel, verify rendering

### Level 4: Edge Cases
```
- Long text (does it wrap?)
- Missing optional fields (does it still render?)
- International characters (do they display?)
- Special characters (are they escaped?)
```

---

## Validation Script (Python)

Quick script to validate JSON before posting:

```python
import json
from slack_sdk import WebClient

def validate_blocks(blocks):
    """Validate Block Kit JSON structure"""

    issues = []

    # Check JSON validity
    try:
        json_str = json.dumps(blocks)
    except TypeError as e:
        issues.append(f"Invalid JSON: {e}")
        return issues

    # Check block count
    if len(blocks) > 100:
        issues.append(f"Too many blocks: {len(blocks)} (max 100)")

    # Check for required fields
    for i, block in enumerate(blocks):
        if "type" not in block:
            issues.append(f"Block {i}: Missing 'type' field")

        block_type = block.get("type")

        # Check block-specific requirements
        if block_type == "section" and "text" not in block and "fields" not in block:
            issues.append(f"Block {i}: Section must have 'text' or 'fields'")

        if block_type == "input":
            if "block_id" not in block:
                issues.append(f"Block {i}: Input must have 'block_id'")
            if "label" not in block:
                issues.append(f"Block {i}: Input must have 'label'")
            if "element" not in block:
                issues.append(f"Block {i}: Input must have 'element'")

    return issues

# Usage
blocks = [...]  # Your JSON blocks
issues = validate_blocks(blocks)

if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ Validation passed!")
```

---

## Slack API Error Messages

### Common Error Messages & Solutions

**"invalid_blocks"**
- [ ] Check JSON syntax (missing quotes, commas)
- [ ] Verify block types are valid
- [ ] Check that all required fields present

**"no_text"**
- [ ] Section blocks need `text` or `fields`
- [ ] Text objects need `text` field

**"invalid_action_id"**
- [ ] action_id must be unique
- [ ] action_id required for buttons and form elements
- [ ] action_id must match regex: `^[a-zA-Z0-9_-]*$`

**"invalid_block_id"**
- [ ] block_id must be unique (if present)
- [ ] block_id must match regex: `^[a-zA-Z0-9_-]*$`

**"missing_scope"**
- [ ] Your Slack app needs correct permissions
- [ ] For chat.postMessage: needs `chat:write` scope
- [ ] For modals: needs `views:write` scope

---

## Debugging Workflow

**When something doesn't work:**

1. **Validate JSON syntax**
   - Copy to Block Kit Builder
   - Check for green checkmark

2. **Check variable substitution**
   - Print JSON before sending (Python)
   - Check variable values are correct
   - Verify JSON syntax after substitution

3. **Check permissions**
   - Does bot have needed scopes?
   - Is bot in the channel?
   - Does user have permission?

4. **Review error message**
   - Check Slack app logs
   - Look for specific field causing error
   - Cross-reference with Block Kit docs

5. **Simplify and test**
   - Remove optional fields
   - Test with minimal JSON
   - Add back complexity gradually

---

## Quick Reference Validation Checklist

**Before deploying any Block Kit JSON:**

**Syntax:**
- [ ] Valid JSON (no missing commas/quotes)
- [ ] Block Kit Builder green checkmark

**Structure:**
- [ ] Correct block types for surface
- [ ] Block count under limit
- [ ] All required fields present
- [ ] Unique block_id and action_id values

**Content:**
- [ ] Text not empty
- [ ] URLs complete (https://)
- [ ] Alt text for images
- [ ] Button labels descriptive

**Variables:**
- [ ] Correct substitution syntax
- [ ] Variables match actual field names
- [ ] Escaped special characters

**Testing:**
- [ ] Tested in Block Kit Builder
- [ ] Visual layout correct
- [ ] Tested in actual N8N/Python
- [ ] Tested in actual Slack

---

**Next:** Review [blocks-reference.md](blocks-reference.md) for specific block validation, or [variables-and-templating.md](variables-and-templating.md) for variable substitution validation.

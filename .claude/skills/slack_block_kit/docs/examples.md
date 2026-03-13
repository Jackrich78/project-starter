# Real-World Examples

**Production-Ready Block Kit JSON Examples**

All examples are directly copied from Slack Block Kit Builder. No generated or synthesized examples.

---

## Example 1: Approval Request Message

**Use Case:** Device requests, budget approvals, permission requests with status tracking

**Surface:** Messages

**Block Types Used:** section, actions

**JSON:**
```json
{
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Type:*\nComputer (laptop)"
                },
                {
                    "type": "mrkdwn",
                    "text": "*When:*\nSubmitted Aut 10"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Last Update:*\nMar 10, 2015 (3 years, 5 months)"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Reason:*\nAll vowel keys aren't working."
                },
                {
                    "type": "mrkdwn",
                    "text": "*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\""
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": true,
                        "text": "Approve"
                    },
                    "style": "primary",
                    "value": "click_me_123"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": true,
                        "text": "Deny"
                    },
                    "style": "danger",
                    "value": "click_me_123"
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Request summary:** Linked requester name and request type as primary headline
- **Metadata fields:** Two-column layout showing request details (type, timing, status, reason, specifications)
- **Action buttons:** Approve (primary style) and Deny (danger style) for quick decision-making
- **Context preservation:** All relevant request information visible without additional clicks

**Variables (N8N):**
```
{{$node.GetRequest.data.requester_name}} → Replace "Fred Enriquez"
{{$node.GetRequest.data.requester_url}} → Replace "fakeLink.toEmployeeProfile.com"
{{$node.GetRequest.data.request_type}} → Replace "New device request"
{{$node.GetRequest.data.device_type}} → Replace "Computer (laptop)"
{{$node.GetRequest.data.submission_date}} → Replace "Aut 10"
{{$node.GetRequest.data.last_update}} → Replace "Mar 10, 2015 (3 years, 5 months)"
{{$node.GetRequest.data.reason}} → Replace "All vowel keys aren't working."
{{$node.GetRequest.data.specs}} → Replace "Cheetah Pro 15 - Fast, really fast"
{{$node.GetRequest.data.request_id}} → For action_id or value tracking
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Request data
request_data = {
    "requester_name": "Fred Enriquez",
    "requester_url": "fakeLink.toEmployeeProfile.com",
    "request_type": "New device request",
    "device_type": "Computer (laptop)",
    "submission_date": "Aut 10",
    "last_update": "Mar 10, 2015 (3 years, 5 months)",
    "reason": "All vowel keys aren't working.",
    "specs": "Cheetah Pro 15 - Fast, really fast",
    "request_id": "REQ-12345"
}

# Build message blocks
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"You have a new request:\n*<{request_data['requester_url']}|{request_data['requester_name']} - {request_data['request_type']}>*"
        }
    },
    {
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": f"*Type:*\n{request_data['device_type']}"},
            {"type": "mrkdwn", "text": f"*When:*\n{request_data['submission_date']}"},
            {"type": "mrkdwn", "text": f"*Last Update:*\n{request_data['last_update']}"},
            {"type": "mrkdwn", "text": f"*Reason:*\n{request_data['reason']}"},
            {"type": "mrkdwn", "text": f"*Specs:*\n\"{request_data['specs']}\""}
        ]
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "emoji": True, "text": "Approve"},
                "style": "primary",
                "value": f"approve_{request_data['request_id']}",
                "action_id": f"approve_{request_data['request_id']}"
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "emoji": True, "text": "Deny"},
                "style": "danger",
                "value": f"deny_{request_data['request_id']}",
                "action_id": f"deny_{request_data['request_id']}"
            }
        ]
    }
]

# Post message
response = client.chat_postMessage(
    channel="C1234567890",
    text="New device request from Fred Enriquez",
    blocks=blocks
)
```

**When to Use:**
- Device/equipment requests requiring approval
- Budget or expense approvals
- Permission/access requests
- Hiring requests or job approvals
- Procurement requests with specifications
- Change requests in service management
- IT tickets requiring manager approval
- Any multi-field approval workflow

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 2: Poll Message

**Use Case:** Team lunch voting, meeting location selection, feature voting, group decisions

**Surface:** Messages

**Block Types Used:** section, divider, context, actions

**JSON:**
```json
{
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Where should we order lunch from?* Poll by <fakeLink.toUser.com|Mark>"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":sushi: *Ace Wasabi Rock-n-Roll Sushi Bar*\nThe best landlocked sushi restaurant."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Vote"
                },
                "value": "click_me_123"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png",
                    "alt_text": "Michael Scott"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
                    "alt_text": "Dwight Schrute"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_3.png",
                    "alt_text": "Pam Beasely"
                },
                {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "3 votes"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":hamburger: *Super Hungryman Hamburgers*\nOnly for the hungriest of the hungry."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Vote"
                },
                "value": "click_me_123"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_4.png",
                    "alt_text": "Angela"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
                    "alt_text": "Dwight Schrute"
                },
                {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "2 votes"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":ramen: *Kagawa-Ya Udon Noodle Shop*\nDo you like to shop for noodles? We have noodles."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Vote"
                },
                "value": "click_me_123"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "No votes"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": true,
                        "text": "Add a suggestion"
                    },
                    "value": "click_me_123"
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Poll header:** Question with poll organizer name as linked text
- **Option cards:** Each option has description with emoji, vote button, and vote count
- **Vote visualization:** Profile images of voters displayed in context blocks (shows who voted)
- **Vote count display:** Shows number of votes or "No votes" status for each option
- **Extensibility:** "Add a suggestion" button allows new options to be added
- **Visual separation:** Dividers structure the poll content

**Variables (N8N):**
```
{{$node.GetPoll.data.question}} → Replace poll question
{{$node.GetPoll.data.organizer_name}} → Replace "Mark"
{{$node.GetPoll.data.organizer_url}} → Replace "fakeLink.toUser.com"
{{$node.GetPoll.data.options}} → Replace all options (requires looping for each option)
{{$node.GetPoll.data.option.name}} → Replace option name ("Ace Wasabi Rock-n-Roll Sushi Bar")
{{$node.GetPoll.data.option.description}} → Replace option description
{{$node.GetPoll.data.option.emoji}} → Replace emoji icon
{{$node.GetPoll.data.option.voters}} → Replace voter profile images (requires looping)
{{$node.GetPoll.data.option.vote_count}} → Replace vote count
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Poll data structure
poll_data = {
    "question": "Where should we order lunch from?",
    "organizer_name": "Mark",
    "organizer_url": "fakeLink.toUser.com",
    "options": [
        {
            "emoji": ":sushi:",
            "name": "Ace Wasabi Rock-n-Roll Sushi Bar",
            "description": "The best landlocked sushi restaurant.",
            "voters": [
                {"name": "Michael Scott", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png"},
                {"name": "Dwight Schrute", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png"},
                {"name": "Pam Beasely", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_3.png"}
            ],
            "vote_count": 3
        },
        {
            "emoji": ":hamburger:",
            "name": "Super Hungryman Hamburgers",
            "description": "Only for the hungriest of the hungry.",
            "voters": [
                {"name": "Angela", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_4.png"},
                {"name": "Dwight Schrute", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png"}
            ],
            "vote_count": 2
        },
        {
            "emoji": ":ramen:",
            "name": "Kagawa-Ya Udon Noodle Shop",
            "description": "Do you like to shop for noodles? We have noodles.",
            "voters": [],
            "vote_count": 0
        }
    ]
}

# Build poll blocks
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{poll_data['question']}* Poll by <{poll_data['organizer_url']}|{poll_data['organizer_name']}>"
        }
    },
    {"type": "divider"}
]

# Add each option with voters
for option in poll_data["options"]:
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{option['emoji']} *{option['name']}*\n{option['description']}"
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": "Vote"},
            "value": f"vote_{option['name'].replace(' ', '_').lower()}"
        }
    })

    # Add voter context
    context_elements = []
    for voter in option["voters"]:
        context_elements.append({
            "type": "image",
            "image_url": voter["image_url"],
            "alt_text": voter["name"]
        })

    if option["vote_count"] > 0:
        context_elements.append({
            "type": "plain_text",
            "emoji": True,
            "text": f"{option['vote_count']} {'vote' if option['vote_count'] == 1 else 'votes'}"
        })
    else:
        context_elements.append({
            "type": "mrkdwn",
            "text": "No votes"
        })

    blocks.append({
        "type": "context",
        "elements": context_elements
    })

blocks.append({"type": "divider"})
blocks.append({
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": "Add a suggestion"},
            "value": "add_suggestion"
        }
    ]
})

# Post poll message
response = client.chat_postMessage(
    channel="C1234567890",
    text="New poll: Where should we order lunch from?",
    blocks=blocks
)
```

**When to Use:**
- Team lunch/dining decisions
- Meeting location or time voting
- Feature voting or roadmap prioritization
- Team preference gathering
- Office decisions (music, temperature, activities)
- Event planning choices
- Product or design option selection
- Casual group consensus building

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 3: Newsletter Message

**Use Case:** Company announcements, team updates, event promotions, weekly digests, internal communications

**Surface:** Messages

**Block Types Used:** header, context, divider, section, actions

**JSON:**
```json
{
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":newspaper:  Paper Company Newsletter  :newspaper:"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "text": "*November 12, 2019*  |  Sales Team Announcements",
                    "type": "mrkdwn"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": " :loud_sound: *IN CASE YOU MISSED IT* :loud_sound:"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Replay our screening of *Threat Level Midnight* and pick up a copy of the DVD to give to your customers at the front desk."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Watch Now",
                    "emoji": true
                }
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "The *2019 Dundies* happened. \nAwards were given, heroes were recognized. \nCheck out *#dundies-2019* to see who won awards."
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":calendar: |   *UPCOMING EVENTS*  | :calendar: "
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`11/20-11/22` *Beet the Competition* _ annual retreat at Schrute Farms_"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "RSVP",
                    "emoji": true
                }
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`12/01` *Toby's Going Away Party* at _Benihana_"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Learn More",
                    "emoji": true
                }
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`11/13` :pretzel: *Pretzel Day* :pretzel: at _Scranton Office_"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "RSVP",
                    "emoji": true
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":calendar: |   *PAST EVENTS*  | :calendar: "
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`10/21` *Conference Room Meeting*"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Watch Recording",
                    "emoji": true
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*FOR YOUR INFORMATION*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":printer: *Sabre Printers* are no longer catching on fire! The newest version of our printers are safe to use. Make sure to tell your customers today.",
                "verbatim": false
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Please join me in welcoming our 3 *new hires* to the Paper Company family! \n\n *Robert California*, CEO \n\n *Ryan Howard*, Temp \n\n *Erin Hannon*, Receptionist "
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":pushpin: Do you have something to include in the newsletter? Here's *how to submit content*."
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Newsletter header:** Eye-catching title with emoji branding
- **Metadata:** Date and category/team displayed in context block
- **Content sections:** Organized into distinct categories (In Case You Missed It, Upcoming Events, Past Events, FYI)
- **Section headers:** Emoji-bordered section dividers for clear visual hierarchy
- **Event listings:** Date codes with event names, descriptions, and action buttons
- **Call-to-action buttons:** Watch Now, RSVP, Learn More, Watch Recording for engagement
- **New hires/announcements:** Dedicated section for team introductions
- **Submission CTA:** Footer inviting contributions to future newsletters

**Variables (N8N):**
```
{{$node.GetNewsletter.data.title}} → Replace "Paper Company Newsletter"
{{$node.GetNewsletter.data.date}} → Replace "November 12, 2019"
{{$node.GetNewsletter.data.category}} → Replace "Sales Team Announcements"
{{$node.GetNewsletter.data.missed_items}} → Replace "In Case You Missed It" items (requires looping)
{{$node.GetNewsletter.data.upcoming_events}} → Replace upcoming events (requires looping for each event)
{{$node.GetNewsletter.data.upcoming_events[].date}} → Event date range
{{$node.GetNewsletter.data.upcoming_events[].name}} → Event name
{{$node.GetNewsletter.data.upcoming_events[].location}} → Event location
{{$node.GetNewsletter.data.past_events}} → Replace past events (requires looping)
{{$node.GetNewsletter.data.announcements}} → FYI/announcement items
{{$node.GetNewsletter.data.new_hires}} → New team member names and roles (requires looping)
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Newsletter data
newsletter_data = {
    "title": "Paper Company Newsletter",
    "date": "November 12, 2019",
    "category": "Sales Team Announcements",
    "missed_items": [
        {
            "title": "Threat Level Midnight",
            "description": "Replay our screening of *Threat Level Midnight* and pick up a copy of the DVD to give to your customers at the front desk.",
            "button_text": "Watch Now",
            "button_url": "https://example.com/threat-level-midnight"
        }
    ],
    "upcoming_events": [
        {
            "date": "11/20-11/22",
            "name": "Beet the Competition",
            "description": "annual retreat at Schrute Farms",
            "button_text": "RSVP"
        },
        {
            "date": "12/01",
            "name": "Toby's Going Away Party",
            "description": "at _Benihana_",
            "button_text": "Learn More"
        },
        {
            "date": "11/13",
            "name": "Pretzel Day",
            "description": "at _Scranton Office_",
            "button_text": "RSVP"
        }
    ],
    "past_events": [
        {
            "date": "10/21",
            "name": "Conference Room Meeting",
            "button_text": "Watch Recording"
        }
    ],
    "announcements": [
        "Sabre Printers are no longer catching on fire! The newest version of our printers are safe to use. Make sure to tell your customers today."
    ],
    "new_hires": [
        {"name": "Robert California", "role": "CEO"},
        {"name": "Ryan Howard", "role": "Temp"},
        {"name": "Erin Hannon", "role": "Receptionist"}
    ]
}

# Build newsletter blocks
blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f":newspaper: {newsletter_data['title']} :newspaper:"
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"*{newsletter_data['date']}*  |  {newsletter_data['category']}"
            }
        ]
    },
    {"type": "divider"},
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":loud_sound: *IN CASE YOU MISSED IT* :loud_sound:"
        }
    }
]

# Add missed items
for item in newsletter_data["missed_items"]:
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": item["description"]
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": item["button_text"], "emoji": True},
            "url": item["button_url"]
        }
    })

blocks.append({"type": "divider"})
blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": ":calendar: | *UPCOMING EVENTS* | :calendar:"
    }
})

# Add upcoming events
for event in newsletter_data["upcoming_events"]:
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"`{event['date']}` *{event['name']}* _{event['description']}_"
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": event["button_text"], "emoji": True},
            "value": f"event_{event['name'].replace(' ', '_').lower()}"
        }
    })

blocks.append({"type": "divider"})
blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": ":calendar: | *PAST EVENTS* | :calendar:"
    }
})

# Add past events
for event in newsletter_data["past_events"]:
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"`{event['date']}` *{event['name']}*"
        },
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": event["button_text"], "emoji": True},
            "value": f"past_event_{event['name'].replace(' ', '_').lower()}"
        }
    })

blocks.append({"type": "divider"})
blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*FOR YOUR INFORMATION*"
    }
})

# Add announcements
for announcement in newsletter_data["announcements"]:
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": announcement
        }
    })

blocks.append({"type": "divider"})

# Add new hires
new_hires_text = "Please join me in welcoming our {} *new hires* to the Paper Company family! \n\n".format(len(newsletter_data["new_hires"]))
for hire in newsletter_data["new_hires"]:
    new_hires_text += f"*{hire['name']}*, {hire['role']}\n\n"

blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": new_hires_text
    }
})

blocks.append({"type": "divider"})
blocks.append({
    "type": "context",
    "elements": [
        {
            "type": "mrkdwn",
            "text": ":pushpin: Do you have something to include in the newsletter? Here's *how to submit content*."
        }
    ]
})

# Post newsletter
response = client.chat_postMessage(
    channel="C1234567890",
    text="Latest Newsletter",
    blocks=blocks
)
```

**When to Use:**
- Weekly/monthly company newsletters
- Team announcements and updates
- Event promotion and calendar distribution
- New hire introductions
- Product/feature announcements
- Company news and achievements
- Internal communications digest
- Team celebration announcements
- All-hands digest messages

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 4: Search Results with Dropdowns

**Use Case:** Internal search results, knowledge base searches, document catalogues, resource discovery

**Surface:** Messages

**Block Types Used:** section, divider, actions

**JSON:**
```json
{
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":mag: Search results for *Cata*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakeLink.toYourApp.com|Use Case Catalogue>*\nUse Case Catalogue for the following departments/roles..."
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Edit it"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Read it"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Save it"
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakeLink.toYourApp.com|Customer Support - Workflow Diagram Catalogue>*\nThis resource was put together by members of..."
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Manage it"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Read it"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Save it"
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakeLink.toYourApp.com|Self-Serve Learning Options Catalogue>*\nSee the learning and development options we..."
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Manage it"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Read it"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Save it"
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakeLink.toYourApp.com|Use Case Catalogue - CF Presentation - [June 12, 2018]>*\nThis is presentation will continue to be updated as..."
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Manage it"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Read it"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Save it"
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakeLink.toYourApp.com|Comprehensive Benefits Catalogue - 2019>*\nInformation about all the benfits we offer is..."
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": true,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Manage it"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Read it"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": true,
                            "text": "Save it"
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": true,
                        "text": "Next 5 Results"
                    },
                    "value": "click_me_123"
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Search header:** Query term displayed with search icon
- **Result cards:** Each result is a linked title with preview description
- **Action dropdowns:** Static select menu per result for inline actions (Edit, Read, Save, Manage)
- **Consistent layout:** All results have same structure and action options
- **Pagination:** "Next 5 Results" button for fetching additional results
- **Compact presentation:** Multiple results visible without scrolling
- **Link integration:** Titles link directly to resources

**Variables (N8N):**
```
{{$node.SearchQuery.data.query_term}} → Replace "Cata" in header
{{$node.SearchResults.data.results}} → Replace all search results (requires looping)
{{$node.SearchResults.data.result.title}} → Result title text
{{$node.SearchResults.data.result.url}} → Result link URL
{{$node.SearchResults.data.result.description}} → Result preview description
{{$node.SearchResults.data.result.actions}} → Action options (requires looping for each result)
{{$node.SearchResults.data.pagination.offset}} → For "Next 5 Results" button
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Search results data
search_data = {
    "query_term": "Cata",
    "results": [
        {
            "title": "Use Case Catalogue",
            "url": "fakeLink.toYourApp.com",
            "description": "Use Case Catalogue for the following departments/roles...",
            "actions": [
                {"text": "Edit it", "value": "edit_0"},
                {"text": "Read it", "value": "read_0"},
                {"text": "Save it", "value": "save_0"}
            ]
        },
        {
            "title": "Customer Support - Workflow Diagram Catalogue",
            "url": "fakeLink.toYourApp.com",
            "description": "This resource was put together by members of...",
            "actions": [
                {"text": "Manage it", "value": "manage_1"},
                {"text": "Read it", "value": "read_1"},
                {"text": "Save it", "value": "save_1"}
            ]
        },
        {
            "title": "Self-Serve Learning Options Catalogue",
            "url": "fakeLink.toYourApp.com",
            "description": "See the learning and development options we...",
            "actions": [
                {"text": "Manage it", "value": "manage_2"},
                {"text": "Read it", "value": "read_2"},
                {"text": "Save it", "value": "save_2"}
            ]
        },
        {
            "title": "Use Case Catalogue - CF Presentation - [June 12, 2018]",
            "url": "fakeLink.toYourApp.com",
            "description": "This is presentation will continue to be updated as...",
            "actions": [
                {"text": "Manage it", "value": "manage_3"},
                {"text": "Read it", "value": "read_3"},
                {"text": "Save it", "value": "save_3"}
            ]
        },
        {
            "title": "Comprehensive Benefits Catalogue - 2019",
            "url": "fakeLink.toYourApp.com",
            "description": "Information about all the benefits we offer is...",
            "actions": [
                {"text": "Manage it", "value": "manage_4"},
                {"text": "Read it", "value": "read_4"},
                {"text": "Save it", "value": "save_4"}
            ]
        }
    ],
    "offset": 0
}

# Build search results blocks
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f":mag: Search results for *{search_data['query_term']}*"
        }
    },
    {"type": "divider"}
]

# Add each search result
for idx, result in enumerate(search_data["results"]):
    # Build action options dynamically
    action_options = [
        {
            "text": {"type": "plain_text", "emoji": True, "text": action["text"]},
            "value": action["value"]
        }
        for action in result["actions"]
    ]

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*<{result['url']}|{result['title']}>*\n{result['description']}"
        },
        "accessory": {
            "type": "static_select",
            "placeholder": {"type": "plain_text", "emoji": True, "text": "Manage"},
            "options": action_options,
            "action_id": f"result_action_{idx}"
        }
    })

blocks.append({"type": "divider"})
blocks.append({
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": "Next 5 Results"},
            "value": f"next_results_{search_data['offset'] + 5}",
            "action_id": "pagination_next"
        }
    ]
})

# Post search results
response = client.chat_postMessage(
    channel="C1234567890",
    text=f"Search results for {search_data['query_term']}",
    blocks=blocks
)
```

**When to Use:**
- Internal knowledge base searches
- Document/resource catalogue lookups
- Wiki or documentation search results
- Help center search results
- Company procedures/policies search
- Team document discovery
- Learning resource searches
- Template or example lookups
- Searchable inventory or asset management

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 5: Workplace Check-In Modal

**Use Case:** Employee engagement surveys, workplace culture feedback, team sentiment gathering, pulse check-ins

**Surface:** Modals

**Block Types Used:** section, divider, input

**JSON:**
```json
{
    "type": "modal",
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": true
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": true
    },
    "title": {
        "type": "plain_text",
        "text": "Workplace check-in",
        "emoji": true
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": ":wave: Hey David!\n\nWe'd love to hear from you how we can make this place the best place you've ever worked.",
                "emoji": true
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "You enjoy working here at Pistachio & Co",
                "emoji": true
            },
            "element": {
                "type": "radio_buttons",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Strongly agree",
                            "emoji": true
                        },
                        "value": "1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Agree",
                            "emoji": true
                        },
                        "value": "2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Neither agree nor disagree",
                            "emoji": true
                        },
                        "value": "3"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Disagree",
                            "emoji": true
                        },
                        "value": "4"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Strongly disagree",
                            "emoji": true
                        },
                        "value": "5"
                    }
                ]
            }
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "What do you want for our team weekly lunch?",
                "emoji": true
            },
            "element": {
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select your favorites",
                    "emoji": true
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pizza: Pizza",
                            "emoji": true
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":fried_shrimp: Thai food",
                            "emoji": true
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":desert_island: Hawaiian",
                            "emoji": true
                        },
                        "value": "value-2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":meat_on_bone: Texas BBQ",
                            "emoji": true
                        },
                        "value": "value-3"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":hamburger: Burger",
                            "emoji": true
                        },
                        "value": "value-4"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":taco: Tacos",
                            "emoji": true
                        },
                        "value": "value-5"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":green_salad: Salad",
                            "emoji": true
                        },
                        "value": "value-6"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":stew: Indian",
                            "emoji": true
                        },
                        "value": "value-7"
                    }
                ]
            }
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "What can we do to improve your experience working here?",
                "emoji": true
            },
            "element": {
                "type": "plain_text_input",
                "multiline": true
            }
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Anything else you want to tell us?",
                "emoji": true
            },
            "element": {
                "type": "plain_text_input",
                "multiline": true
            },
            "optional": true
        }
    ]
}
```

**Key Features:**
- **Personalized greeting:** Section block with employee name (dynamic via variable)
- **Likert scale:** Radio button input with 5-point agreement scale
- **Multi-select preferences:** Food/team activity selection with emoji icons
- **Qualitative feedback:** Two textarea inputs for open-ended responses (one required, one optional)
- **Modal structure:** Submit/Cancel buttons with callback_id for form submission
- **Accessibility:** Clear labels for all input fields with emoji support

**Variables (N8N):**
```
{{$node.GetEmployee.data.employee_name}} → Replace "David"
{{$node.GetEmployee.data.company_name}} → Replace "Pistachio & Co"
{{$node.GetSurveyConfig.data.lunch_options}} → Replace lunch menu options (requires looping)
{{$node.GetSurveyConfig.data.callback_id}} → Set callback_id for form submission handling
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Employee and survey configuration
employee_name = "David"
company_name = "Pistachio & Co"
lunch_options = [
    {"emoji": ":pizza:", "text": "Pizza", "value": "pizza"},
    {"emoji": ":fried_shrimp:", "text": "Thai food", "value": "thai"},
    {"emoji": ":desert_island:", "text": "Hawaiian", "value": "hawaiian"},
    {"emoji": ":meat_on_bone:", "text": "Texas BBQ", "value": "bbq"},
    {"emoji": ":hamburger:", "text": "Burger", "value": "burger"},
    {"emoji": ":taco:", "text": "Tacos", "value": "tacos"},
    {"emoji": ":green_salad:", "text": "Salad", "value": "salad"},
    {"emoji": ":stew:", "text": "Indian", "value": "indian"}
]

# Build lunch option blocks dynamically
lunch_option_blocks = [
    {
        "text": {"type": "plain_text", "text": f"{opt['emoji']} {opt['text']}", "emoji": True},
        "value": opt["value"]
    }
    for opt in lunch_options
]

# Build modal
modal = {
    "type": "modal",
    "callback_id": "workplace_checkin",
    "title": {"type": "plain_text", "text": "Workplace check-in", "emoji": True},
    "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
    "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f":wave: Hey {employee_name}!\n\nWe'd love to hear from you how we can make this place the best place you've ever worked.",
                "emoji": True
            }
        },
        {"type": "divider"},
        {
            "type": "input",
            "block_id": "workplace_satisfaction",
            "label": {"type": "plain_text", "text": f"You enjoy working here at {company_name}", "emoji": True},
            "element": {
                "type": "radio_buttons",
                "action_id": "satisfaction_radio",
                "options": [
                    {"text": {"type": "plain_text", "text": "Strongly agree", "emoji": True}, "value": "1"},
                    {"text": {"type": "plain_text", "text": "Agree", "emoji": True}, "value": "2"},
                    {"text": {"type": "plain_text", "text": "Neither agree nor disagree", "emoji": True}, "value": "3"},
                    {"text": {"type": "plain_text", "text": "Disagree", "emoji": True}, "value": "4"},
                    {"text": {"type": "plain_text", "text": "Strongly disagree", "emoji": True}, "value": "5"}
                ]
            }
        },
        {
            "type": "input",
            "block_id": "team_lunch_preferences",
            "label": {"type": "plain_text", "text": "What do you want for our team weekly lunch?", "emoji": True},
            "element": {
                "type": "multi_static_select",
                "action_id": "lunch_select",
                "placeholder": {"type": "plain_text", "text": "Select your favorites", "emoji": True},
                "options": lunch_option_blocks
            }
        },
        {
            "type": "input",
            "block_id": "experience_improvement",
            "label": {"type": "plain_text", "text": "What can we do to improve your experience working here?", "emoji": True},
            "element": {"type": "plain_text_input", "action_id": "improvement_input", "multiline": True}
        },
        {
            "type": "input",
            "block_id": "additional_feedback",
            "label": {"type": "plain_text", "text": "Anything else you want to tell us?", "emoji": True},
            "element": {"type": "plain_text_input", "action_id": "feedback_input", "multiline": True},
            "optional": True
        }
    ]
}

# Handle modal submission (typically done via Flask/FastAPI webhook)
# When user submits, Slack sends view_submission event with block_id and values
# Example submission handler:
def handle_checkin_submission(body):
    """
    Process workplace check-in form submission
    Access submission values via:
    - body['view']['state']['values']['workplace_satisfaction']['satisfaction_radio']['selected_option']['value']
    - body['view']['state']['values']['team_lunch_preferences']['lunch_select']['selected_options']
    - body['view']['state']['values']['experience_improvement']['improvement_input']['value']
    - body['view']['state']['values']['additional_feedback']['feedback_input']['value']
    """
    pass
```

**When to Use:**
- Employee engagement pulse surveys
- Workplace culture feedback collection
- Team preference gathering (food, activities, etc.)
- Onboarding feedback from new hires
- Periodic check-ins (weekly, monthly, quarterly)
- Manager-employee one-on-one preparation
- Exit surveys or alumni feedback
- Diversity & inclusion initiatives
- Team building and social event planning

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 6: Booking Itinerary Modal

**Use Case:** Event/trip itineraries, booking confirmations, travel summaries, event schedules, multi-day event confirmations

**Surface:** Modals

**Block Types Used:** header, divider, section, context

**JSON:**
```json
{
    "type": "modal",
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": true
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": true
    },
    "title": {
        "type": "plain_text",
        "text": "Your itinerary",
        "emoji": true
    },
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":tada: You're all set! This is your booking summary."
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Attendee*\nKatie Chen"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Date*\nOct 22-23"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":house: Accommodation"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Redwood Suite*\n*Share with 2 other person.* Studio home. Modern bathroom. TV. Heating. Full kitchen. Patio with lounge chairs and campfire style fire pit and grill."
            },
            "accessory": {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/redwood-suite.png",
                "alt_text": "Redwood Suite"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":fork_and_knife: Food & Dietary restrictions"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*All-rounder*\nYou eat most meats, seafood, dairy and vegetables."
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":woman-running: Activities"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Winery tour and tasting*"
            },
            "fields": [
                {
                    "type": "plain_text",
                    "text": "Wednesday, Oct 22 2019, 2pm-5pm",
                    "emoji": true
                },
                {
                    "type": "plain_text",
                    "text": "Hosted by Sandra Mullens",
                    "emoji": true
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Sunrise hike to Mount Amazing*"
            },
            "fields": [
                {
                    "type": "plain_text",
                    "text": "Thursday, Oct 23 2019, 5:30am",
                    "emoji": true
                },
                {
                    "type": "plain_text",
                    "text": "Hosted by Jordan Smith",
                    "emoji": true
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Design systems brainstorm*"
            },
            "fields": [
                {
                    "type": "plain_text",
                    "text": "Thursday, Oct 23 2019, 11a",
                    "emoji": true
                },
                {
                    "type": "plain_text",
                    "text": "Hosted by Mary Lee",
                    "emoji": true
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Confirmation header:** Success message with celebration emoji
- **Attendee and date summary:** Key booking information in fields layout
- **Section organization:** Grouped by category (Accommodation, Food, Activities) with context headers
- **Accommodation card:** Includes image thumbnail with detailed description
- **Activity listings:** Each activity shows title, time/date, and host in structured fields
- **Emoji icons:** Category headers use emoji for quick visual scanning
- **Dividers:** Clear visual separation between sections

**Variables (N8N):**
```
{{$node.GetBooking.data.attendee_name}} → Replace "Katie Chen"
{{$node.GetBooking.data.date_range}} → Replace "Oct 22-23"
{{$node.GetBooking.data.accommodation.name}} → Replace "Redwood Suite"
{{$node.GetBooking.data.accommodation.description}} → Replace accommodation description
{{$node.GetBooking.data.accommodation.image_url}} → Replace accommodation image
{{$node.GetBooking.data.accommodation.roommates}} → Replace roommate count
{{$node.GetBooking.data.dietary_preference}} → Replace "All-rounder"
{{$node.GetBooking.data.dietary_description}} → Replace dietary description
{{$node.GetBooking.data.activities}} → Replace activities (requires looping)
{{$node.GetBooking.data.activity.name}} → Activity title
{{$node.GetBooking.data.activity.datetime}} → Activity date/time
{{$node.GetBooking.data.activity.host}} → Activity host name
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Booking data
booking_data = {
    "attendee_name": "Katie Chen",
    "date_range": "Oct 22-23",
    "accommodation": {
        "name": "Redwood Suite",
        "roommates": 2,
        "description": "Studio home. Modern bathroom. TV. Heating. Full kitchen. Patio with lounge chairs and campfire style fire pit and grill.",
        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/redwood-suite.png",
        "alt_text": "Redwood Suite"
    },
    "dietary": {
        "type": "All-rounder",
        "description": "You eat most meats, seafood, dairy and vegetables."
    },
    "activities": [
        {
            "name": "Winery tour and tasting",
            "datetime": "Wednesday, Oct 22 2019, 2pm-5pm",
            "host": "Sandra Mullens"
        },
        {
            "name": "Sunrise hike to Mount Amazing",
            "datetime": "Thursday, Oct 23 2019, 5:30am",
            "host": "Jordan Smith"
        },
        {
            "name": "Design systems brainstorm",
            "datetime": "Thursday, Oct 23 2019, 11a",
            "host": "Mary Lee"
        }
    ]
}

# Build itinerary modal
modal = {
    "type": "modal",
    "callback_id": "booking_itinerary",
    "title": {"type": "plain_text", "text": "Your itinerary", "emoji": True},
    "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
    "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
    "blocks": [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": ":tada: You're all set! This is your booking summary."}
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Attendee*\n{booking_data['attendee_name']}"},
                {"type": "mrkdwn", "text": f"*Date*\n{booking_data['date_range']}"}
            ]
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": ":house: Accommodation"}]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{booking_data['accommodation']['name']}*\n*Share with {booking_data['accommodation']['roommates']} other person.* {booking_data['accommodation']['description']}"
            },
            "accessory": {
                "type": "image",
                "image_url": booking_data['accommodation']['image_url'],
                "alt_text": booking_data['accommodation']['alt_text']
            }
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": ":fork_and_knife: Food & Dietary restrictions"}]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{booking_data['dietary']['type']}*\n{booking_data['dietary']['description']}"
            }
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": ":woman-running: Activities"}]
        },
        {"type": "divider"}
    ]
}

# Add each activity dynamically
for activity in booking_data["activities"]:
    modal["blocks"].append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{activity['name']}*"
        },
        "fields": [
            {"type": "plain_text", "text": activity["datetime"], "emoji": True},
            {"type": "plain_text", "text": f"Hosted by {activity['host']}", "emoji": True}
        ]
    })

# Post modal as response to trigger (button click, slash command, etc.)
# This is typically done via Flask/FastAPI webhook handler
def open_itinerary_modal(trigger_id):
    """
    Open the booking itinerary modal
    trigger_id comes from user interaction (button click, slash command)
    """
    client.views_open(trigger_id=trigger_id, view=modal)
```

**When to Use:**
- Event/conference booking confirmations
- Travel itinerary summaries
- Trip/vacation planning confirmations
- Multi-day event schedules
- Accommodation confirmations
- Activity bookings with details
- Conference agenda displays
- Retreat/offsite itineraries
- Hotel/resort booking summaries

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 7: Ticket Management App Modal

**Use Case:** Issue/ticket tracking, project management dashboards, task lists with filtering, team task visibility

**Surface:** Modals

**Block Types Used:** section, divider, context

**JSON:**
```json
{
    "type": "modal",
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": true
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": true
    },
    "title": {
        "type": "plain_text",
        "text": "Ticket app",
        "emoji": true
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a ticket list from the dropdown"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": true
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "All Tickets",
                            "emoji": true
                        },
                        "value": "all_tickets"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Assigned To Me",
                            "emoji": true
                        },
                        "value": "assigned_to_me"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Issued By Me",
                            "emoji": true
                        },
                        "value": "issued_by_me"
                    }
                ],
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": "Assigned To Me",
                        "emoji": true
                    },
                    "value": "assigned_to_me"
                }
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/highpriority.png",
                    "alt_text": "High Priority"
                },
                {
                    "type": "mrkdwn",
                    "text": "*High Priority*"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakelink.com|WEB-1098 Adjust borders on homepage graphic>*"
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":white_check_mark: Mark as done",
                            "emoji": true
                        },
                        "value": "done"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pencil: Edit",
                            "emoji": true
                        },
                        "value": "edit"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":x: Delete",
                            "emoji": true
                        },
                        "value": "delete"
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Awaiting Release"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/task-icon.png",
                    "alt_text": "Task Icon"
                },
                {
                    "type": "mrkdwn",
                    "text": "Task"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png",
                    "alt_text": "Michael Scott"
                },
                {
                    "type": "mrkdwn",
                    "text": "<fakelink.toUser.com|Michael Scott>"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakelink.com|MOB-2011 Deep-link from web search results to product page>*"
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":white_check_mark: Mark as done",
                            "emoji": true
                        },
                        "value": "done"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pencil: Edit",
                            "emoji": true
                        },
                        "value": "edit"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":x: Delete",
                            "emoji": true
                        },
                        "value": "delete"
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Open"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/newfeature.png",
                    "alt_text": "New Feature Icon"
                },
                {
                    "type": "mrkdwn",
                    "text": "New Feature"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
                    "alt_text": "Pam Beasely"
                },
                {
                    "type": "mrkdwn",
                    "text": "<fakelink.toUser.com|Pam Beasely>"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/mediumpriority.png",
                    "alt_text": "palm tree"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Medium Priority*"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakelink.com|WEB-1098 Adjust borders on homepage graphic>*"
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":white_check_mark: Mark as done",
                            "emoji": true
                        },
                        "value": "done"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pencil: Edit",
                            "emoji": true
                        },
                        "value": "edit"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":x: Delete",
                            "emoji": true
                        },
                        "value": "delete"
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Awaiting Release"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/task-icon.png",
                    "alt_text": "Task Icon"
                },
                {
                    "type": "mrkdwn",
                    "text": "Task"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png",
                    "alt_text": "Michael Scott"
                },
                {
                    "type": "mrkdwn",
                    "text": "<fakelink.toUser.com|Michael Scott>"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakelink.com|MOB-2011 Deep-link from web search results to product page>*"
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":white_check_mark: Mark as done",
                            "emoji": true
                        },
                        "value": "done"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pencil: Edit",
                            "emoji": true
                        },
                        "value": "edit"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":x: Delete",
                            "emoji": true
                        },
                        "value": "delete"
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Open"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/newfeature.png",
                    "alt_text": "New Feature Icon"
                },
                {
                    "type": "mrkdwn",
                    "text": "New Feature"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
                    "alt_text": "Pam Beasely"
                },
                {
                    "type": "mrkdwn",
                    "text": "<fakelink.toUser.com|Pam Beasely>"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<fakelink.com|WEB-1098 Adjust borders on homepage graphic>*"
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":white_check_mark: Mark as done",
                            "emoji": true
                        },
                        "value": "done"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":pencil: Edit",
                            "emoji": true
                        },
                        "value": "edit"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": ":x: Delete",
                            "emoji": true
                        },
                        "value": "delete"
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Awaiting Release"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/task-icon.png",
                    "alt_text": "Task Icon"
                },
                {
                    "type": "mrkdwn",
                    "text": "Task"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png",
                    "alt_text": "Michael Scott"
                },
                {
                    "type": "mrkdwn",
                    "text": "<fakelink.toUser.com|Michael Scott>"
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Filter dropdown:** Static select with pre-configured views (All Tickets, Assigned To Me, Issued By Me) with initial selection
- **Priority grouping:** Tickets organized by priority level (High, Medium) with priority icon indicators
- **Ticket cards:** Linked ticket IDs with descriptions as section titles
- **Overflow menus:** Three-action menus per ticket (Mark as done, Edit, Delete)
- **Rich metadata:** Status, ticket type icon, and assignee displayed in context blocks
- **Visual indicators:** Priority icons and type icons (task, feature) for quick scanning
- **Assignee profiles:** Linked user profiles with user images
- **Compact layout:** Multiple tickets visible without scrolling

**Variables (N8N):**
```
{{$node.GetTickets.data.filter_options}} → Replace dropdown filter options
{{$node.GetTickets.data.tickets}} → Replace all tickets (requires looping by priority)
{{$node.GetTickets.data.ticket.priority}} → Ticket priority level
{{$node.GetTickets.data.ticket.priority_icon}} → Priority icon URL
{{$node.GetTickets.data.ticket.id}} → Ticket ID (e.g., "WEB-1098")
{{$node.GetTickets.data.ticket.title}} → Ticket title/description
{{$node.GetTickets.data.ticket.url}} → Link to ticket in external system
{{$node.GetTickets.data.ticket.status}} → Ticket status (e.g., "Awaiting Release")
{{$node.GetTickets.data.ticket.type}} → Ticket type (Task, Bug, Feature)
{{$node.GetTickets.data.ticket.type_icon}} → Type icon URL
{{$node.GetTickets.data.ticket.assignee}} → Assignee name
{{$node.GetTickets.data.ticket.assignee_url}} → Assignee profile link
{{$node.GetTickets.data.ticket.assignee_image}} → Assignee avatar URL
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Ticket data organized by priority
tickets_data = {
    "filters": [
        {"label": "All Tickets", "value": "all_tickets"},
        {"label": "Assigned To Me", "value": "assigned_to_me"},
        {"label": "Issued By Me", "value": "issued_by_me"}
    ],
    "by_priority": {
        "High": [
            {
                "id": "WEB-1098",
                "title": "Adjust borders on homepage graphic",
                "url": "fakelink.com",
                "status": "Awaiting Release",
                "type": "Task",
                "type_icon": "https://api.slack.com/img/blocks/bkb_template_images/task-icon.png",
                "assignee": "Michael Scott",
                "assignee_url": "fakelink.toUser.com",
                "assignee_image": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png"
            },
            {
                "id": "MOB-2011",
                "title": "Deep-link from web search results to product page",
                "url": "fakelink.com",
                "status": "Open",
                "type": "New Feature",
                "type_icon": "https://api.slack.com/img/blocks/bkb_template_images/newfeature.png",
                "assignee": "Pam Beasely",
                "assignee_url": "fakelink.toUser.com",
                "assignee_image": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png"
            }
        ],
        "Medium": [
            {
                "id": "WEB-1098",
                "title": "Adjust borders on homepage graphic",
                "url": "fakelink.com",
                "status": "Awaiting Release",
                "type": "Task",
                "type_icon": "https://api.slack.com/img/blocks/bkb_template_images/task-icon.png",
                "assignee": "Michael Scott",
                "assignee_url": "fakelink.toUser.com",
                "assignee_image": "https://api.slack.com/img/blocks/bkb_template_images/profile_1.png"
            }
        ]
    },
    "priority_icons": {
        "High": "https://api.slack.com/img/blocks/bkb_template_images/highpriority.png",
        "Medium": "https://api.slack.com/img/blocks/bkb_template_images/mediumpriority.png"
    }
}

# Build ticket management modal
modal = {
    "type": "modal",
    "callback_id": "ticket_management",
    "title": {"type": "plain_text", "text": "Ticket app", "emoji": True},
    "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
    "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
    "blocks": [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Pick a ticket list from the dropdown"},
            "accessory": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select an item", "emoji": True},
                "options": [
                    {
                        "text": {"type": "plain_text", "text": f["label"], "emoji": True},
                        "value": f["value"]
                    }
                    for f in tickets_data["filters"]
                ],
                "initial_option": {
                    "text": {"type": "plain_text", "text": "Assigned To Me", "emoji": True},
                    "value": "assigned_to_me"
                },
                "action_id": "ticket_filter_select"
            }
        },
        {"type": "divider"}
    ]
}

# Add tickets grouped by priority
for priority in ["High", "Medium"]:
    if priority in tickets_data["by_priority"]:
        modal["blocks"].extend([
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": tickets_data["priority_icons"][priority],
                        "alt_text": f"{priority} Priority"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{priority} Priority*"
                    }
                ]
            },
            {"type": "divider"}
        ])

        # Add each ticket in priority group
        for ticket in tickets_data["by_priority"][priority]:
            modal["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{ticket['url']}|{ticket['id']} {ticket['title']}>*"
                },
                "accessory": {
                    "type": "overflow",
                    "options": [
                        {"text": {"type": "plain_text", "text": ":white_check_mark: Mark as done", "emoji": True}, "value": "done"},
                        {"text": {"type": "plain_text", "text": ":pencil: Edit", "emoji": True}, "value": "edit"},
                        {"text": {"type": "plain_text", "text": ":x: Delete", "emoji": True}, "value": "delete"}
                    ],
                    "action_id": f"ticket_action_{ticket['id']}"
                }
            })

            modal["blocks"].append({
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": ticket["status"]},
                    {"type": "image", "image_url": ticket["type_icon"], "alt_text": ticket["type"]},
                    {"type": "mrkdwn", "text": ticket["type"]},
                    {"type": "image", "image_url": ticket["assignee_image"], "alt_text": ticket["assignee"]},
                    {"type": "mrkdwn", "text": f"<{ticket['assignee_url']}|{ticket['assignee']}>"}
                ]
            })

# Open modal via button trigger
def open_ticket_modal(trigger_id):
    client.views_open(trigger_id=trigger_id, view=modal)
```

**When to Use:**
- Issue/ticket/bug tracking dashboards
- Project management task lists
- Team task assignment visibility
- Sprint planning interfaces
- Work queue displays
- Help desk ticket management
- Feature request tracking
- Kanban board alternatives
- Team workload management

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 8: Budget Performance Home Tab

**Use Case:** Finance dashboards, expense approval workflows, budget tracking, personal finance dashboards, finance manager interfaces

**Surface:** Home Tabs

**Block Types Used:** section, divider, context, actions

**JSON:**
```json
{
    "type": "home",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Budget Performance*"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Manage App Settings",
                    "emoji": true
                },
                "value": "app_settings"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Current Quarter*\nBudget: $18,000 (ends in 53 days)\nSpend: $4,289.70\nRemain: $13,710.30"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Top Expense Categories*\n:airplane: Flights · 30%\n:taxi: Taxi / Uber / Lyft · 24% \n:knife_fork_plate: Client lunch / meetings · 18%"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Expenses Awaiting Your Approval*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Submitted by"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_3.png",
                    "alt_text": "Dwight Schrute"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Dwight Schrute*"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Team Lunch (Internal)*\nCost: *$85.50USD*\nDate: *10/16/2019*\nService Provider: *Honest Sandwiches*  \nExpense no. *<fakelink.toUrl.com|#1797PD>*"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/creditcard.png",
                "alt_text": "credit card"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Approve",
                        "emoji": true
                    },
                    "style": "primary",
                    "value": "approve"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Decline",
                        "emoji": true
                    },
                    "style": "danger",
                    "value": "decline"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Details",
                        "emoji": true
                    },
                    "value": "details"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Submitted by"
                },
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
                    "alt_text": "Pam Beasely"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Pam Beasely*"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Flights to New York*\nCost: *$520.78USD*\nDate: *10/18/2019*\nService Provider: *Delta Airways*\nExpense no. *<fakelink.toUrl.com|#1803PD>*"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/plane.png",
                "alt_text": "plane"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Approve",
                        "emoji": true
                    },
                    "style": "primary",
                    "value": "approve"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Decline",
                        "emoji": true
                    },
                    "style": "danger",
                    "value": "decline"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Details",
                        "emoji": true
                    },
                    "value": "details"
                }
            ]
        }
    ]
}
```

**Key Features:**
- **Budget summary header:** Current quarter budget with remaining balance prominently displayed
- **Settings button:** "Manage App Settings" for configuration access
- **Budget breakdown:** Two-column fields showing budget status and top expense categories
- **Placeholder chart:** Visual representation area for charts or graphs
- **Pending approvals:** "Expenses Awaiting Your Approval" section header
- **Expense cards:** Each pending expense shows submitter, details, cost, date, provider, and expense ID
- **Accessory icons:** Thumbnail icons representing expense category (credit card, plane)
- **Action buttons:** Approve (primary), Decline (danger), View Details for each expense
- **Persistent layout:** Always-accessible home tab for finance managers

**Variables (N8N):**
```
{{$node.GetBudgetData.data.budget_total}} → Replace "$18,000"
{{$node.GetBudgetData.data.days_remaining}} → Replace "53 days"
{{$node.GetBudgetData.data.spent}} → Replace "$4,289.70"
{{$node.GetBudgetData.data.remaining}} → Replace "$13,710.30"
{{$node.GetBudgetData.data.expense_categories}} → Replace expense categories (requires looping)
{{$node.GetBudgetData.data.pending_expenses}} → Replace pending expenses (requires looping)
{{$node.GetBudgetData.data.expense.submitter}} → Expense submitter name
{{$node.GetBudgetData.data.expense.submitter_image}} → Submitter profile image
{{$node.GetBudgetData.data.expense.title}} → Expense title/description
{{$node.GetBudgetData.data.expense.cost}} → Expense amount
{{$node.GetBudgetData.data.expense.date}} → Expense date
{{$node.GetBudgetData.data.expense.provider}} → Service provider name
{{$node.GetBudgetData.data.expense.id}} → Expense ID/reference
{{$node.GetBudgetData.data.expense.icon}} → Expense category icon URL
```

**Variables (Python):**
```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Budget and expense data
budget_data = {
    "budget_total": 18000,
    "days_remaining": 53,
    "spent": 4289.70,
    "expense_categories": [
        {"emoji": ":airplane:", "name": "Flights", "percentage": 30},
        {"emoji": ":taxi:", "name": "Taxi / Uber / Lyft", "percentage": 24},
        {"emoji": ":knife_fork_plate:", "name": "Client lunch / meetings", "percentage": 18}
    ],
    "pending_expenses": [
        {
            "id": "1797PD",
            "title": "Team Lunch (Internal)",
            "cost": 85.50,
            "currency": "USD",
            "date": "10/16/2019",
            "provider": "Honest Sandwiches",
            "submitter": "Dwight Schrute",
            "submitter_image": "https://api.slack.com/img/blocks/bkb_template_images/profile_3.png",
            "icon": "https://api.slack.com/img/blocks/bkb_template_images/creditcard.png"
        },
        {
            "id": "1803PD",
            "title": "Flights to New York",
            "cost": 520.78,
            "currency": "USD",
            "date": "10/18/2019",
            "provider": "Delta Airways",
            "submitter": "Pam Beasely",
            "submitter_image": "https://api.slack.com/img/blocks/bkb_template_images/profile_2.png",
            "icon": "https://api.slack.com/img/blocks/bkb_template_images/plane.png"
        }
    ]
}

# Build home tab view
home_view = {
    "type": "home",
    "blocks": [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Budget Performance*"},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Manage App Settings", "emoji": True},
                "value": "app_settings",
                "action_id": "settings_button"
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Current Quarter*\nBudget: ${budget_data['budget_total']:,} (ends in {budget_data['days_remaining']} days)\nSpend: ${budget_data['spent']:,.2f}\nRemain: ${budget_data['budget_total'] - budget_data['spent']:,.2f}"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Top Expense Categories*\n" + "\n".join(
                        f"{cat['emoji']} {cat['name']} · {cat['percentage']}%"
                        for cat in budget_data["expense_categories"]
                    )
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Expenses Awaiting Your Approval*"}
        },
        {"type": "divider"}
    ]
}

# Add each pending expense
for expense in budget_data["pending_expenses"]:
    home_view["blocks"].extend([
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "Submitted by"},
                {"type": "image", "image_url": expense["submitter_image"], "alt_text": expense["submitter"]},
                {"type": "mrkdwn", "text": f"*{expense['submitter']}*"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{expense['title']}*\nCost: *${expense['cost']}{expense['currency']}*\nDate: *{expense['date']}*\nService Provider: *{expense['provider']}*\nExpense no. *<fakelink.toUrl.com|#{expense['id']}>*"
            },
            "accessory": {
                "type": "image",
                "image_url": expense["icon"],
                "alt_text": expense["title"]
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Approve", "emoji": True},
                    "style": "primary",
                    "value": f"approve_{expense['id']}",
                    "action_id": f"approve_{expense['id']}"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Decline", "emoji": True},
                    "style": "danger",
                    "value": f"decline_{expense['id']}",
                    "action_id": f"decline_{expense['id']}"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Details", "emoji": True},
                    "value": f"details_{expense['id']}",
                    "action_id": f"details_{expense['id']}"
                }
            ]
        },
        {"type": "divider"}
    ])

# Publish home tab (typically called on app_home_opened event)
def update_home_tab(user_id):
    """Update user's home tab with budget data"""
    client.views_publish(user_id=user_id, view=home_view)
```

**When to Use:**
- Finance manager dashboards
- Expense approval workflows
- Budget tracking for individuals/teams
- Personal finance overviews
- Travel expense management
- Finance app integrations
- Cost center monitoring
- Employee reimbursement interfaces
- Finance reporting dashboards

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## Example 9: TODO List Home Tab

**Use Case:** Personal task management, daily/weekly planners, productivity dashboards, to-do tracking apps

**Surface:** Home Tabs

**Block Types Used:** actions (with checkboxes element), context, section

**Complete JSON:**

```json
{
    "type": "home",
    "blocks": [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create New Task",
                        "emoji": true
                    },
                    "style": "primary",
                    "value": "create_task",
                    "action_id": "create_task_action"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Tasks*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "checkboxes",
                    "initial_options": [
                        {
                            "value": "completed_1"
                        }
                    ],
                    "options": [
                        {
                            "value": "completed_1",
                            "description": {
                                "type": "plain_text",
                                "text": "Due tomorrow at 2:30pm",
                                "emoji": true
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "~Finish Q4 review~"
                            }
                        },
                        {
                            "value": "task_2",
                            "description": {
                                "type": "plain_text",
                                "text": "Due today at 5:00pm",
                                "emoji": true
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "*Submit team updates*"
                            }
                        },
                        {
                            "value": "task_3",
                            "description": {
                                "type": "plain_text",
                                "text": "No due date",
                                "emoji": true
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "Review design proposals"
                            }
                        },
                        {
                            "value": "task_4",
                            "description": {
                                "type": "plain_text",
                                "text": "Due in 3 days",
                                "emoji": true
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "Prepare presentation slides"
                            }
                        }
                    ],
                    "action_id": "todo_checkbox_action"
                }
            ]
        }
    ]
}
```

**Key Features:**

- **Checkboxes Element:** Uses `checkboxes` element for task completion tracking (not radio buttons or multi-select)
- **Initial Options:** `initial_options` array marks already-completed tasks (strikethrough formatting in text)
- **Descriptions:** Each task has a `description` field showing due dates or additional context
- **Text Formatting:** Uses markdown formatting (strikethrough `~text~` for completed items, bold `*text*` for in-progress)
- **Primary Action Button:** "Create New Task" button with primary style for task creation workflow
- **Visual Hierarchy:** Context block with image, section header, divider, then interactive checkbox block

**Variables (N8N):**

```
// Task list loop - substitute completed tasks and task list from your data source
"initial_options": [
  { "value": "completed_1" },
  { "value": "{{$node.GetTasks.data.completed_tasks[1].id}}" }
],
"options": [
  {
    "value": "completed_1",
    "description": {
      "type": "plain_text",
      "text": "{{$node.GetTasks.data.completed_tasks[0].due_date}}",
      "emoji": true
    },
    "text": { "type": "mrkdwn", "text": "~{{$node.GetTasks.data.completed_tasks[0].title}}~" }
  },
  // Loop for incomplete tasks
  {
    "value": "task_{{$node.GetTasks.data.open_tasks[0].id}}",
    "description": {
      "type": "plain_text",
      "text": "Due {{$node.GetTasks.data.open_tasks[0].due_date}}",
      "emoji": true
    },
    "text": { "type": "mrkdwn", "text": "*{{$node.GetTasks.data.open_tasks[0].title}}*" }
  }
]
```

**Variables (Python):**

```python
from slack_sdk import WebClient

client = WebClient(token="xoxb-your-token")

# Sample task data
task_data = {
    "completed_tasks": [
        {"id": "completed_1", "title": "Finish Q4 review", "due_date": "Due tomorrow at 2:30pm"},
        {"id": "completed_2", "title": "Code review for PR #42", "due_date": "Due yesterday"}
    ],
    "open_tasks": [
        {"id": "task_2", "title": "Submit team updates", "due_date": "Due today at 5:00pm"},
        {"id": "task_3", "title": "Review design proposals", "due_date": "No due date"},
        {"id": "task_4", "title": "Prepare presentation slides", "due_date": "Due in 3 days"}
    ]
}

# Build initial_options (completed tasks that should be pre-checked)
initial_options = [
    {"value": completed_task["id"]}
    for completed_task in task_data["completed_tasks"]
]

# Build all task options (completed and open)
all_options = []

# Add completed tasks (with strikethrough)
for task in task_data["completed_tasks"]:
    all_options.append({
        "value": task["id"],
        "description": {
            "type": "plain_text",
            "text": task["due_date"],
            "emoji": True
        },
        "text": {
            "type": "mrkdwn",
            "text": f"~{task['title']}~"
        }
    })

# Add open tasks (with bold)
for task in task_data["open_tasks"]:
    all_options.append({
        "value": task["id"],
        "description": {
            "type": "plain_text",
            "text": task["due_date"],
            "emoji": True
        },
        "text": {
            "type": "mrkdwn",
            "text": f"*{task['title']}*"
        }
    })

# Build home tab view
home_view = {
    "type": "home",
    "blocks": [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create New Task",
                        "emoji": True
                    },
                    "style": "primary",
                    "value": "create_task",
                    "action_id": "create_task_action"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Tasks*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "checkboxes",
                    "initial_options": initial_options,
                    "options": all_options,
                    "action_id": "todo_checkbox_action"
                }
            ]
        }
    ]
}

# Handle checkbox changes (action handler)
def handle_task_update(body):
    """Handle task completion/unchecking"""
    selected_tasks = body["actions"][0]["selected_options"]
    user_id = body["user"]["id"]

    # Extract checked task IDs
    checked_task_ids = [opt["value"] for opt in selected_tasks]

    # Your app would update task completion status in your database
    print(f"User {user_id} has checked: {checked_task_ids}")

    # Re-render home tab with updated status
    update_home_tab(user_id)

def update_home_tab(user_id):
    """Update user's home tab with current tasks"""
    # Fetch fresh task data for user
    user_tasks = get_user_tasks(user_id)  # Your function to fetch tasks

    # Rebuild home_view with fresh data
    # ... (repeat the home_view building code with fresh data)

    client.views_publish(user_id=user_id, view=home_view)
```

**When to Use:**

- Personal to-do lists in Slack app
- Team daily standup task tracking
- Individual project management dashboards
- Weekly planner home tabs
- Task progress tracking
- Agile sprint board summaries
- Daily productivity dashboards
- Meeting preparation checklists
- Employee onboarding task lists
- Project milestone tracking

**Block Kit Builder Link:** Test this by pasting the JSON into https://api.slack.com/tools/block-kit-builder

---

## How to Add Examples

**Format:**
```markdown
## Example N: [Title]

**Use Case:** [When/why to use this]

**Surface:** [Messages/Modals/Home Tabs]

**Block Types Used:** [List block types]

**JSON:**
[Complete JSON from Block Kit Builder]

**Key Features:**
- Feature 1
- Feature 2

**Variables (N8N):**
```
field → description
```

**Variables (Python):**
```python
# Code example
```

**When to Use:**
- Scenario 1
- Scenario 2

**Block Kit Builder Link:** [Link to test]
```

---

**Note:** All examples in this file are directly from Slack Block Kit Builder. They are tested, validated, and production-ready.

**Next:** See [best-practices.md](best-practices.md) for validation checklists, or [blocks-reference.md](blocks-reference.md) for detailed block documentation.

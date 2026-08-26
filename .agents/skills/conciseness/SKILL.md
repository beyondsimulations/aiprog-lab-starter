---
name: conciseness
description: Identifies wordiness, redundant phrases, and unnecessary filler in academic writing. Use when tightening prose or reducing word count.
---

When asked to apply this skill to a text, review the provided academic text for conciseness opportunities.

## Common Wordiness Patterns

### Redundant Phrases
| Wordy | Concise |
|-------|---------|
| in order to | to |
| due to the fact that | because |
| at this point in time | now/currently |
| in the event that | if |
| for the purpose of | to/for |
| in spite of the fact that | although/despite |
| the reason is because | because |
| in close proximity to | near |
| a large number of | many |
| the vast majority of | most |
| in the absence of | without |
| has the ability to | can |
| it is important to note that | [delete or] notably |
| it should be noted that | [delete] |
| as a matter of fact | [delete] |

### Filler Words (often deletable)
- very, really, quite, rather, somewhat
- basically, essentially, actually, certainly
- specific, particular, given (when vague)
- clearly, obviously (unless emphasizing)

### Nominalizations (verb → noun padding)
| Wordy | Concise |
|-------|---------|
| make a decision | decide |
| conduct an analysis | analyze |
| perform an evaluation | evaluate |
| give consideration to | consider |
| reach a conclusion | conclude |
| make an assumption | assume |

### Expletive Constructions
| Wordy | Concise |
|-------|---------|
| There are many factors that... | Many factors... |
| It is clear that X... | X clearly... / Clearly, X... |
| It was found that... | We found... / Results showed... |

## Output Format

### Inline Suggestions

For each issue found:

**Line/Section:** "wordy phrase" → "concise alternative"
- Saved: [N words]
- Pattern: [redundancy/filler/nominalization/etc.]

### Summary

| Pattern | Count | Words Saved |
|---------|-------|-------------|
| Redundant phrases | N | ~N |
| Filler words | N | ~N |
| Nominalizations | N | ~N |
| Expletive constructions | N | ~N |
| **Total potential savings** | | **~N words** |

## Guidelines

- Prioritize changes that improve clarity, not just brevity
- Some "wordiness" aids readability; don't over-compress
- Consider emphasis: sometimes extra words serve a purpose
- Academic writing allows some formality that seems wordy in other contexts
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.

---
name: academic-grammar
description: Checks text for grammar mistakes, wording issues, and scientific language best practices. Use when reviewing academic writing for grammar, style, or scientific conventions.
---

When asked to apply this skill to a text, review the provided academic text for grammar and scientific writing quality.

## What to Check

1. **Grammar errors**: Subject-verb agreement, article usage, punctuation, sentence fragments
2. **Awkward phrasing**: Unclear or convoluted sentences that hinder readability
3. **Scientific language**: Ensure formal, objective tone appropriate for academic writing
4. **Common academic mistakes**:
   - Avoid contractions (don't → do not)
   - Avoid informal language (a lot → numerous, get → obtain)
   - Avoid first person only where the target venue disallows it — many STEM/CS venues now accept "we" (otherwise: I found → The results indicate)
   - Avoid vague quantifiers (some, many → specific numbers or "several")
   - Avoid rhetorical questions
   - Avoid split infinitives when awkward

## Output Format

### Inline Suggestions

For each issue found:

**Line/Section:** "original text" → "suggested text"
- Reason: [brief explanation]

### Summary

| Issue Type | Count | Examples |
|------------|-------|----------|
| Grammar | N | [brief examples] |
| Informal language | N | [brief examples] |
| Awkward phrasing | N | [brief examples] |
| Scientific style | N | [brief examples] |

## Guidelines

- Focus on errors that affect clarity or professionalism
- Don't flag stylistic preferences that are acceptable
- Prioritize issues by severity (errors > style > minor polish)
- Be specific about why something is problematic
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.

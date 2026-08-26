---
name: hedging-language
description: Checks academic writing for appropriate hedging of claims. Use when reviewing whether statements are appropriately qualified or when checking for overclaiming.
---

When asked to apply this skill to a text, review the provided academic text for appropriate hedging of claims.

## Hedging Spectrum

| Level | Language | Use When |
|-------|----------|----------|
| Strong claim | "X causes Y", "proves", "demonstrates" | Direct experimental evidence, established facts |
| Moderate hedge | "X suggests", "indicates", "supports" | Strong correlational evidence, replicated findings |
| Cautious hedge | "X may", "might", "could", "appears to" | Preliminary findings, indirect evidence |
| Tentative | "X seems to", "tends to", "is possible" | Speculative interpretation, limited data |

## What to Check

### Overclaiming (needs more hedging)
- Causal language without experimental design ("X causes Y" from correlational data)
- Universal statements ("always", "never", "all") without sufficient evidence
- "Proves" or "proof" (science rarely proves, it supports/suggests)
- Definitive conclusions from single studies

### Under-hedging phrases to flag
- "clearly shows" → "suggests" or "indicates"
- "proves that" → "provides evidence that"
- "definitely" → "likely" or remove
- "the fact that" → "the finding that" (when not established fact)

### Over-hedging (may need strengthening)
- Excessive hedging on well-established facts
- Multiple hedges in one sentence ("may possibly suggest")
- Hedging your own direct observations/measurements

## Output Format

### Inline Suggestions

For each issue found:

**Line/Section:** "original claim" → "suggested revision"
- Issue: [Overclaiming/Under-hedging/Over-hedging]
- Reason: [why this level of certainty is inappropriate]

### Summary

| Issue Type | Count | Impact |
|------------|-------|--------|
| Overclaiming | N | [High/Medium] - affects credibility |
| Over-hedging | N | [Low/Medium] - weakens valid claims |

## Guidelines

- Consider the evidence presented when judging appropriate hedging
- Discipline norms vary; some fields hedge more than others
- Hedging in conclusions should match strength of evidence in results
- Don't over-correct; some confident statements are warranted
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.

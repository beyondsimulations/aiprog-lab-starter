---
name: acronym-check
description: Verifies that acronyms are defined on first use and used consistently throughout academic writing. Use when checking acronym usage or preparing manuscripts for submission.
---

Review the provided academic text for proper acronym usage.

## Rules to Check

1. **Definition on first use**: Every acronym must be spelled out on first use
   - Format: "Full Term (ACRONYM)" on first occurrence
   - Exception: Universally known acronyms (DNA, USA, etc.) may not need definition

2. **Consistency after definition**: Once defined, use the acronym consistently
   - Don't switch back to full form randomly
   - Don't redefine the same acronym

3. **Abstract independence**: Acronyms in abstract should be redefined if used in body
   - Abstracts are often read separately from the paper

4. **Acronym necessity**: Avoid defining acronyms used fewer than 3-4 times
   - If rarely used, just spell it out each time

5. **No orphan definitions**: Don't define an acronym and never use it again

6. **Standard acronyms**: Check that acronyms match standard usage in the field

## Common Issues

| Issue | Example | Fix |
|-------|---------|-----|
| Undefined acronym | "The API failed" (first use) | "The Application Programming Interface (API) failed" |
| Double definition | Defined in abstract AND body identically | Keep both (abstracts are standalone) |
| Orphan definition | "Random Forest (RF)" then never use "RF" | Remove "(RF)" or use the acronym |
| Inconsistent form | "ML" and "machine learning" mixed | Pick one after definition |
| Over-acronyming | "We used SM (Statistical Methods)" | Don't acronym common phrases |

## Output Format

### Inline Suggestions

For each issue found:

**Line/Section:** [issue description]
- Issue type: [Undefined/Orphan/Inconsistent/Unnecessary]
- Suggestion: [specific fix]

### Summary

#### Acronym Inventory

| Acronym | Full Form | First Defined | Times Used | Status |
|---------|-----------|---------------|------------|--------|
| [ACR] | [Full Form] | Line N / Not defined | N | [OK/Issue] |

#### Issues Found

| Issue Type | Count | Acronyms Affected |
|------------|-------|-------------------|
| Undefined | N | [list] |
| Orphan definitions | N | [list] |
| Inconsistent usage | N | [list] |
| Unnecessary acronyms | N | [list] |

## Guidelines

- Field-standard acronyms (e.g., "GDP" in economics) may not need definition
- Journal guidelines may specify acronym rules
- Tables and figures may need independent acronym definitions
- Consider reader expertise when deciding what needs definition
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.

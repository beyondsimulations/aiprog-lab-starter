---
name: model-formulation
description: Reviews optimization and mathematical model formulations for correctness and completeness. Use when checking objective functions, constraints, and variable definitions.
---

Review the provided mathematical model formulation for correctness and completeness.

## What to Check

### 1. Objective Function
- Clearly stated as minimization or maximization
- Well-defined for all feasible solutions
- Matches the stated problem goal
- Linear/nonlinear nature acknowledged if relevant

### 2. Decision Variables
- All variables explicitly listed
- Domain specified for each variable:
  - Continuous: x ∈ ℝ or x ≥ 0
  - Integer: x ∈ ℤ
  - Binary: x ∈ {0,1}
  - Bounded: l ≤ x ≤ u
- Variables match their use in constraints/objective

### 3. Parameters
- Clearly distinguished from decision variables
- Values or ranges specified
- Data source mentioned where appropriate

### 4. Index Sets
- All index sets defined with their elements
- Cardinality specified where relevant
- Consistent indexing throughout model

### 5. Constraints
- All constraints necessary for the problem
- No redundant constraints
- Proper inequality/equality operators
- Constraint qualifications noted (∀i, ∈ I, etc.)
- Bound constraints included

### 6. Model Completeness Checklist
- [ ] Feasibility: Does a feasible solution exist?
- [ ] Boundedness: Is the objective bounded?
- [ ] Non-negativity: Are appropriate variables non-negative?
- [ ] Integrality: Are integer requirements specified?
- [ ] Linking constraints: Are related variables properly linked?

### 7. Notation Conventions
- "subject to" or "s.t." used consistently
- Constraint numbering/labeling consistent
- Standard optimization notation followed

## Output Format

### Inline Suggestions

For each issue found:

**Model component:** [objective/constraint/variable]
- Problem: [what's missing or incorrect]
- Impact: [how this affects model validity]
- Suggestion: [how to fix]

### Summary

#### Model Structure

| Component | Status | Notes |
|-----------|--------|-------|
| Objective | [OK/Issue] | [notes] |
| Variables | [OK/Issue] | [N variables, domains specified?] |
| Parameters | [OK/Issue] | [N parameters, values given?] |
| Constraints | [OK/Issue] | [N constraints] |
| Index sets | [OK/Issue] | [defined?] |

#### Issues Found

| Issue Type | Count | Severity |
|------------|-------|----------|
| Missing variable domains | N | High |
| Undefined parameters | N | Medium |
| Constraint gaps | N | High |
| Notation inconsistencies | N | Low |

## Guidelines

- Consider standard formulations in the field
- Check for common modeling errors (big-M issues, linearization correctness)
- Verify that the model actually solves the stated problem
- Note any assumptions that should be made explicit

- Show proposed edits as a diff or a list; do not rewrite the document wholesale.

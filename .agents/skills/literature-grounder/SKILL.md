---
name: literature-grounder
description: Ground academic claims (thesis chapters, papers, workshop materials) in research literature with proper citations, flagging unsupported claims rather than inventing sources. Use when adding citations, checking whether a claim is supported, or when the user asks to "ground this in literature," "find a citation for," or "check if this claim is supported."
---

# Literature Grounder

When asked to apply this skill to a text, ground its claims in research literature using this systematic approach.

## 1. Identify Claims Needing Evidence

Flag statements that are:
- **Factual claims**: Statistics, measurements, thresholds, capacities
- **Causal claims**: "X causes Y", "X leads to Y"
- **Best practices**: "Research shows...", "Studies indicate..."
- **Definitions**: Technical terms, frameworks, models

## 2. Search the Project's Literature Sources First

Before reaching for general knowledge, search the project itself for the specific claim in question. Look for a literature/references folder or bibliography file in the project — common names include `references.bib`, `bibliography.bib`, `literature/`, `sources/`, `md_literature/`, and `grounding/`. If none of these exists, ask the user where their citation library lives rather than guessing.

Search these files for the exact claim (grep for keywords, then read the matching excerpt) and pull only the relevant quote plus its citation key — do not read entire literature files start to finish when a targeted search will do. Work from the citation keys already present in the project's `.bib` file and flag anything that would require a new source (see Section 7). Never fabricate a citation to fill a gap.

## 3. Citation Hierarchy (Prefer Higher)

1. **Systematic reviews / Meta-analyses** - Strongest evidence
2. **Peer-reviewed empirical studies** - Primary research
3. **Official guidelines / Standards** - Authoritative for practice
4. **Textbooks / Handbooks** - Good for established knowledge
5. **Expert opinion / White papers** - Use when primary sources unavailable

## 4. Citation Format

Use BibTeX citation keys in the format `@author_keyword_year`:
- Single author: `@helbing_pedestrian_2013`
- Multiple authors: `@feliciani_introduction_2021`
- Organizations: `@rcmc_crowd_management_2025`

In Quarto/Markdown: `According to [@author_year], the effect is...`

Match the citation-key format to the project's actual `.bib` file — use the keys that already exist there rather than inventing a new key convention.

## 5. Grounding Checklist

For each major claim, ensure:
- [ ] Source is identified (or marked as needing citation)
- [ ] Citation key exists in references.bib (or needs to be added)
- [ ] Claim accurately represents the source (no overgeneralization)
- [ ] Page/section number noted for specific facts

## 6. When Sources Conflict

- Acknowledge the disagreement explicitly
- Prefer more recent systematic evidence
- Note context differences (e.g., "In Western contexts... but in Hajj settings...")
- Consider citing multiple sources: `[@source1; @source2]`

## 7. Flagging Gaps

When evidence is missing, mark it explicitly rather than inventing a source:
```markdown
<!-- CITATION NEEDED: [specific claim] -->
```

Or in speaker notes:
```markdown
::: {.notes}
Note: This claim requires citation support. Check [topic area] literature.
:::
```

Never fabricate a reference to fill a gap. A visible "citation needed" marker is always preferable to an invented one — inventing citations is a serious integrity failure, not a shortcut.

## Output Format

When grounding content, provide:
1. A summary of citations added or gaps flagged, with the exact `[@key]` inserted at each location
2. Show proposed edits as a diff or a list (quoted line + citation added); do not rewrite the document wholesale
3. Any gaps flagged for follow-up

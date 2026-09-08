# DollarTemplates Paper Composition Architecture

## Executive Summary

The current engine’s abstractions were too workflow-oriented. They described business widgets like `WritingArea`, `Checklist`, `ActionItems`, and `FieldRow`, but the visual language of reMarkable templates is not organized around business semantics. It is organized around paper composition.

The redesigned engine is therefore centered on four ideas:

1. A page has structure.
2. A page is composed of regions.
3. Regions define how content is written.
4. Devices define constraints, not content.

This shifts the framework from “template generation” toward a paper composition engine.

---

## Reverse-Engineered Visual Grammar

Across the observed templates, the visual language is consistent:

### 1. Shared page structure

The page is always a calm, mostly empty canvas with:

- very small labels
- generous writing space
- thin divider rules
- controlled whitespace
- minimal, almost invisible UI
- strong alignment
- strong margins
- restrained typography

### 2. Recurring layouts

The templates repeatedly reuse a small set of spatial patterns:

- `canvas` — one large writing field
- `stack` — vertical flow of meaningful sections
- `split` — two large panes with a shared relationship
- `quadrants` — four equal regions for parallel thinking
- `sidebar` — one primary zone plus one secondary zone
- `table` — structured rows and columns
- `planner` — repeated rows with labels and spaces
- `timeline` — sequential or ordered flow
- `flow` — task or process progression

These are not business concepts. They are page patterns.

### 3. Recurring spacing

The grammar is driven by spacing more than by decoration.

Common characteristics:

- tight top/bottom page padding
- thin rules that feel like guidance rather than UI
- clear, generous internal breathing room
- near-constant rule opacity and stroke weight
- proportional spacing between content blocks and writing blocks

In practice, the engine is not trying to draw “forms”; it is trying to preserve the feel of paper.

### 4. Recurring alignment

The observed templates align content in a strict, disciplined way:

- labels align to the left edge of a region
- text fields align with fixed baselines
- horizontal rules extend across available width
- writing regions stay within safe areas
- columns, when used, are equally distributed or intentionally weighted

This is a key insight: the framework should optimize for alignment before it optimizes for semantics.

### 5. Recurring regions

Most page structures can be decomposed into a handful of region roles:

- `metadata` — fields like date, meeting, people, subject
- `section` — a labeled semantic group
- `reference` — contextual reminder or guide text
- `writing` — primary handwriting area
- `checklist` — checkbox or list-led region
- `table` — rows and columns
- `sidebar` — contextual secondary panel
- `footer` — page footer or provenance line
- `header` — minimal top content or title area

A region’s role is about paper meaning, not business domain.

### 6. Recurring writing patterns

The templates consistently favor simple writing styles:

- blank regions
- ruled lines
- dotted guidance
- grid guidance
- checkboxes
- tables
- numbered or bulleted tracks

The same region can change style based on the intended use, without changing the rest of the page structure.

### 7. Typography

Typography is intentionally restrained.

Common traits:

- tiny labels
- small uppercase headers
- minimal decoration
- no heavy emphasis except for structure
- very subtle footers or provenance text

This makes the page disappear and lets handwriting dominate.

### 8. Recurring page structures

The most reusable structures discovered are:

1. `canvas`
2. `stack`
3. `split`
4. `quadrants`
5. `sidebar`
6. `table`
7. `planner`
8. `timeline`
9. `flow`

The current engine already contains implicit examples of these: the meeting notes flow is a vertical stack with metadata, grouped writing, and action items; the SOAP layout is a quadrants composition; future templates like planners and timelines can emerge from the same grammar.

---

## Architectural Redesign

### Problem with the previous model

The previous API forced developers to think in terms of business widgets:

- `WritingArea`
- `Checklist`
- `ActionItems`
- `FieldRow`

Those are useful helpers, but they are not the real abstraction boundary. They are surface-level conveniences for certain workflows.

The framework should instead model:

- how the page is composed
- what regions exist
- how each region behaves
- what writing style it employs

### New composition model

The engine now supports:

- `Page`
- `Region`
- `WritingStyle`

with a backward-compatible legacy `sections` path still preserved.

This gives the framework the correct responsibility split:

- `Template` describes the semantic intention of the document
- `Page` describes the physical composition of the page
- `Region` describes where content lives on paper
- `WritingStyle` describes how the region behaves as paper
- `Renderer` decides the SVG output
- `Device` supplies constraints

### Proposed responsibility boundaries

```
Template
  ↓
Page Composition
  ↓
Regions
  ↓
Writing Style
  ↓
Renderer
  ↓
Device
  ↓
Output (SVG → PNG/PDF)
```

This is cleaner than the old widget-first design because every layer owns one concern.

---

## Why this is better

### 1. Better semantics

A developer now describes paper, not a business process.

The question becomes:

- How is the page composed?
- What regions exist?
- How should each region behave?
- How should people write inside them?

That is much closer to how professional paper design works.

### 2. Better reuse

The same primitives can now build:

- SWOT
- SOAP
- Meeting Minutes
- Peer Review
- Pros / Cons
- Kanban
- Weekly Planner
- Project Planning
- Quadrant Method
- Feedback Model

without introducing template-specific renderer logic.

### 3. Better testability

The engine now has a cleaner model for validating:

- schema
- safe areas
- overlap
- rendering
- deterministic geometry
- visual output

### 4. Better device adaptation

Devices still define constraints, but the page composition model can adapt elegantly across devices without forcing templates to care about hardware details.

---

## Current Refactor Status

The framework has already been updated in the codebase to support the paper composition model.

### Added in the domain layer

- `Page`
- `Region`
- `WritingStyle`

### Renderer changes

The SVG renderer now supports page composition rendering, while preserving the legacy sections-driven rendering path for backwards compatibility.

### Compatibility layer

Legacy templates remain valid and continue to render. The new model is additive rather than disruptive.

### Tests

A new regression test was added to validate the paper composition API and confirm that a page-based template can render with the same safety guarantees as legacy templates.

---

## Recommended next evolution

The next architectural step is to formalize the page grammar as a richer set of reusable composition helpers, such as:

- `header_stack`
- `split_columns`
- `quadrant_page`
- `planner_rows`
- `timeline_flow`

Those would be composition constructors rather than template-specific features.

At that point, the engine would genuinely become a paper composition engine rather than a template system.

---

## Design Principles

The architecture should continue to follow these rules:

1. Templates describe intention.
2. Pages describe structure.
3. Regions describe paper zones.
4. Writing styles describe behavior.
5. Devices define constraints.
6. Renderers produce SVG.
7. PNG and PDF are derived outputs.
8. Geometry belongs in layout, not in templates.
9. Visual language should remain minimal and paper-like.

---

## Conclusion

The original engine had the right goal but the wrong abstraction boundary. It modeled workflows instead of paper.

The redesign moves the framework toward the correct abstraction:

- paper-first
- region-driven
- writing-style-aware
- device-agnostic
- composition-oriented

That is the foundation that will allow DollarTemplates Engine to become a professional paper composition engine for every supported e-ink device.

# DollarTemplates Engine

> **Design templates once. Deploy them to every e-ink device.**

DollarTemplates Engine is a Python framework for building beautiful digital paper for e-ink tablets.

Instead of manually designing a different template for every device, you define your template **semantically** and let the engine automatically render, validate, test, and package it for every supported e-ink device.

The framework is built around three principles:

- **Minimal** — Remove everything that doesn't help the user think.
- **Intentional** — Every section has a purpose.
- **Focused** — One template, one job.

---

# Vision

Creating digital paper today is fragmented.

Every device has different dimensions, safe areas, toolbars, resolutions and quirks. Template creators end up maintaining dozens of nearly identical files.

DollarTemplates solves this by separating:

- **What the template is**
- **Where it is rendered**

A Meeting Notes template should simply describe:

- Meeting
- Agenda
- Decisions
- Action Items
- Notes

—not pixel coordinates.

The engine determines how that template should look on each supported device.

Design once.

Deploy everywhere.

---

## Paper Composition Architecture

The framework has been refactored toward a paper-first model.

Instead of organizing the engine around business widgets like `WritingArea`, `Checklist`, and `ActionItems`, the architecture now centers on:

- `Page` — how the sheet is composed
- `Region` — what meaningful area of paper exists
- `WritingStyle` — how each region behaves as paper
- `Template` — the higher-level semantic intention

This means the engine now models paper grammar directly, while preserving the legacy `sections` API for compatibility.

A new design analysis document is available in [docs/paper-composition-architecture.md](docs/paper-composition-architecture.md).

---

# Architecture

```
                Template
                    │
                    ▼
         Semantic Components
                    │
                    ▼
             Layout Engine
                    │
                    ▼
             Device Profile
                    │
                    ▼
              Validation
                    │
                    ▼
                 Renderer
          ┌────────┼────────┐
          ▼        ▼        ▼
         SVG      PNG      PDF
```

The architecture follows one fundamental rule:

> **Templates define content. Devices define constraints. Renderers decide presentation.**

This means adding a new device should never require redesigning existing templates.

---

# Current Features

## Templates

- Meeting Notes
- SOAP Note

## Supported Devices

- reMarkable Paper Pro Move
- reMarkable 2

## Semantic Components

Currently supported:

- `FieldRow`
- `Checklist`
- `WritingArea`
- `ActionItems`

Future components:

- Field
- Divider
- Table
- Rating
- Timeline
- Calendar
- Progress
- Signature
- NumberedList
- BulletedList
- DatePicker
- TimeField

## Rendering

Current outputs:

- SVG
- PNG
- PDF

## Validation

Built-in validation includes:

- Schema validation
- Safe-area validation
- Layout validation
- Overlap detection
- Deterministic rendering
- Visual regression testing

---

# Project Structure

```
dollartemplates/

├── components/
├── devices/
│   ├── registry.py
│   └── remarkable/
│
├── renderers/
│
├── templates/
│
├── validators/
│
├── tests/
│
└── cli.py
```

---

# Setup

## macOS

### 1. Clone the repository

```bash
git clone <repository-url>
cd dollartemplates-python-v1.0
```

### 2. Install Homebrew (if needed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 3. Install Cairo

```bash
brew install cairo
```

Verify:

```bash
brew --prefix cairo
```

Expected:

```
/opt/homebrew/opt/cairo
```

### 4. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 6. Configure Cairo (if necessary)

If you receive:

```
OSError: no library called "cairo"
```

run:

```bash
export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix cairo)/lib:$DYLD_FALLBACK_LIBRARY_PATH"
```

To make this permanent:

```bash
echo 'export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix cairo)/lib:$DYLD_FALLBACK_LIBRARY_PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -e ".[dev]"
```

> Install the Cairo runtime before generating PNG or PDF outputs.

---

# Verify Installation

```bash
dt devices

dt templates

pytest -q
```

Expected:

```
paper-pro-move
remarkable-2
```

If the tests complete without failures, the engine is correctly installed.

---

# Creating Templates

Create a new template:

```bash
dt new one-on-one
```

Edit:

```
src/dollartemplates/templates/one_on_one.py
```

Example:

```python
from dollartemplates.components import (
    FieldRow,
    WritingArea,
    ActionItems,
)

from dollartemplates.models import Template


one_on_one = Template(

    id="one-on-one",

    title="1:1",

    supported_devices=[
        "paper-pro-move",
    ],

    sections=[

        FieldRow([
            "Person",
            "Date",
        ]),

        WritingArea(
            "Wins",
            size="medium",
        ),

        WritingArea(
            "Challenges",
            size="medium",
        ),

        ActionItems(
            rows=3,
        ),

        WritingArea(
            "Notes",
            size="large",
            expandable=True,
        ),
    ],
)
```

---

# Building Templates

Build for one device:

```bash
dt build meeting-notes --device paper-pro-move
```

Build every supported device:

```bash
dt build soap-note --all
```

Generate PDFs as well:

```bash
dt build soap-note --all --pdf
```

Output:

```
output/

    meeting-notes/

        paper-pro-move/
            meeting-notes.svg
            meeting-notes.png
            meeting-notes.pdf

        remarkable-2/
            meeting-notes.svg
            meeting-notes.png
            meeting-notes.pdf
```

---

# Adding Devices

Adding a new device should only require:

1. Create a device profile

```
devices/<brand>/<device>.py
```

2. Register it

```
devices/registry.py
```

3. Add the device ID to the template

```python
supported_devices=[
    "paper-pro-move",
    "remarkable-2",
]
```

4. Run tests

```bash
pytest
```

5. Build

```bash
dt build meeting-notes --all
```

No layout changes should be required.

---

# Testing & Verification

DollarTemplates treats templates like software.

Every template should pass automated validation before being considered production ready.

Run the complete test suite:

```bash
pytest -q
```

Verbose output:

```bash
pytest -v
```

Specific test:

```bash
pytest tests/test_engine.py -v
```

Keyword filtering:

```bash
pytest -k soap -v
```

---

## What We Test

### Template Schema

Ensures templates are structurally valid.

Examples:

- Template IDs
- Titles
- Component definitions
- Supported device IDs
- Required metadata

---

### Device Contracts

Ensures device definitions are valid.

Examples:

- Width
- Height
- PPI
- Safe areas
- Capabilities

---

### Layout Safety

Every generated page is checked automatically.

Examples:

- No overlap
- No clipping
- Safe-area compliance
- Footer spacing
- Minimum handwriting area
- Content fits page

---

### Render Tests

Ensures outputs are successfully generated.

Examples:

- SVG
- PNG
- PDF

---

### Deterministic Rendering

The exact same template should generate the exact same output unless the template intentionally changes.

This prevents accidental renderer regressions.

---

### Visual Regression

Approved renders become visual baselines.

New renders are automatically compared against the approved version.

Typical failures include:

- shifted sections
- spacing changes
- missing labels
- missing rules
- clipping
- typography changes
- overflow

Intentional changes should be visually reviewed before updating the approved baseline.

---

# Release Checklist

Before marking a template **Verified**:

```bash
pytest -q
```

Generate every supported version:

```bash
dt build <template> --all
```

Review:

```
output/<template>/<device>/
```

Only after:

- Tests pass
- Layout is correct
- Visual comparison passes
- Device review is complete

should a template receive the **Verified** label.

> **Verified is an engineering standard—not a marketing claim.**

---

# Roadmap

## Devices

- reMarkable Paper Pro
- reMarkable Paper Pure
- BOOX
- Kindle Scribe
- Supernote

## Components

- Tables
- Ratings
- Timelines
- Calendars
- Progress bars
- Signatures
- More writing components

## Engine

- Automatic page continuation
- Better typography engine
- Constraint-based layout
- Device capability detection
- Smart spacing optimization

## Testing

- Per-device visual baselines
- Pixel-by-pixel regression reports
- CI test artifacts
- Automatic release verification
- On-device certification workflow

---

# Philosophy

DollarTemplates isn't a collection of templates.

It's an engine for creating digital paper.

Design once.

Deploy everywhere.

Minimal.

Intentional.

Focused.
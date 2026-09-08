import re

import pytest
from dollartemplates.devices.registry import DEVICES
from dollartemplates.templates.registry import TEMPLATES
from dollartemplates.renderers import render_svg
from dollartemplates.validators import validate_template, validate_layout
from dollartemplates.models import Page, Region, WritingStyle, Template

def test_devices_contracts():
    assert (DEVICES["paper-pro-move"].width,DEVICES["paper-pro-move"].height,DEVICES["paper-pro-move"].ppi)==(954,1696,264)
    assert (DEVICES["remarkable-2"].width,DEVICES["remarkable-2"].height,DEVICES["remarkable-2"].ppi)==(1404,1872,226)


def test_remarkable_2_layout_overrides():
    device = DEVICES["remarkable-2"]
    assert device.layout_overrides["heading_size"] == 30
    svg, _ = render_svg(TEMPLATES["meeting-notes"], device)
    assert "MEETING NOTES" not in svg


def test_page_titles_can_be_explicitly_opted_in():
    t = TEMPLATES["meeting-notes"].model_copy(update={"show_page_title": True})
    svg, _ = render_svg(t, DEVICES["paper-pro-move"])
    assert "MEETING NOTES" in svg

@pytest.mark.parametrize("template_id",list(TEMPLATES))
def test_schema(template_id):
    errors,_=validate_template(TEMPLATES[template_id],DEVICES); assert not errors

@pytest.mark.parametrize("template_id",list(TEMPLATES))
def test_expandable_last(template_id):
    t=TEMPLATES[template_id]; xs=[s for s in t.sections if getattr(s,"expandable",False)]; assert len(xs)<=1
    if xs: assert xs[0].id==t.sections[-1].id

@pytest.mark.parametrize("template_id",list(TEMPLATES))
def test_layouts(template_id):
    t=TEMPLATES[template_id]
    for did in t.supported_devices:
        svg,bounds=render_svg(t,DEVICES[did]); errors,_=validate_layout(bounds,DEVICES[did]); assert not errors; assert svg.startswith("<svg")

def test_soap_structure():
    t = TEMPLATES["soap-note"]
    assert t.layout == "quadrant"
    assert [s.label for s in t.sections]==["DATE","SUBJECTIVE","OBJECTIVE","ASSESSMENT","PLAN"]


@pytest.mark.parametrize("template_id", list(TEMPLATES))
def test_writing_area_labels_have_space_for_rules(template_id):
    template = TEMPLATES[template_id]

    for device_id in template.supported_devices:
        svg, _ = render_svg(template, DEVICES[device_id])

        for section in template.sections:
            if section.kind != "writing-area":
                continue

            label_match = re.search(
                rf'<text[^>]*>{re.escape(section.label.upper())}</text>',
                svg,
            )
            assert label_match is not None, f"missing label for {template_id}/{section.label}"

            label_tag = label_match.group(0)
            label_y_match = re.search(r'y="([^"]+)"', label_tag)
            assert label_y_match is not None, f"missing y position for {template_id}/{section.label}"
            label_y = float(label_y_match.group(1))

            remaining_svg = svg[label_match.end():]
            next_line_match = re.search(r'<line[^>]*y1="([^"]+)"', remaining_svg)
            assert next_line_match is not None, f"missing rule lines for {template_id}/{section.label}"

            line_y = float(next_line_match.group(1))
            assert line_y - label_y >= 24, (
                f"{template_id}/{section.label} is too close to the first rule line: {line_y - label_y}px"
            )


def test_page_titles_disabled_by_default():
    svg, _ = render_svg(TEMPLATES["meeting-notes"], DEVICES["paper-pro-move"])
    assert "MEETING NOTES" not in svg
    soap_svg, _ = render_svg(TEMPLATES["soap-note"], DEVICES["paper-pro-move"])
    assert "SOAP NOTE" not in soap_svg


def test_soap_quadrant_layout_bounds():
    t = TEMPLATES["soap-note"]
    for did in t.supported_devices:
        device = DEVICES[did]
        _, bounds = render_svg(t, device)
        errors,_ = validate_layout(bounds, device)
        assert not errors
        quadrant_bounds = [b for b in bounds if b.role in {"subjective", "objective", "assessment", "plan"}]
        widths = [b.width for b in quadrant_bounds]
        heights = [b.height for b in quadrant_bounds]
        assert max(widths) - min(widths) <= 2
        assert max(heights) - min(heights) <= 2


def test_paper_composition_model():
    page = Page(
        layout="quadrants",
        regions=[
            Region(id="subjective", role="writing", title="Subjective", style=WritingStyle(kind="ruled", lines=8)),
            Region(id="objective", role="writing", title="Objective", style=WritingStyle(kind="ruled", lines=8)),
            Region(id="assessment", role="writing", title="Assessment", style=WritingStyle(kind="ruled", lines=8)),
            Region(id="plan", role="writing", title="Plan", style=WritingStyle(kind="ruled", lines=8)),
        ],
    )

    template = Template(
        id="paper-composition",
        title="PAPER COMPOSITION",
        supported_devices=["paper-pro-move", "remarkable-2"],
        page=page,
    )

    for did in template.supported_devices:
        svg, bounds = render_svg(template, DEVICES[did])
        assert svg.startswith("<svg")
        assert {b.role for b in bounds if b.role in {"subjective", "objective", "assessment", "plan"}} == {"subjective", "objective", "assessment", "plan"}

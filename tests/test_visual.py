from pathlib import Path
from dollartemplates.devices.registry import DEVICES
from dollartemplates.templates.registry import TEMPLATES
from dollartemplates.renderers import render_svg, svg_to_png
from dollartemplates.visual import compare_images


def test_meeting_notes_visual(tmp_path):
    baseline = Path(__file__).parent / "visual" / "meeting-notes" / "paper-pro-move" / "approved.png"
    actual = tmp_path / "actual.png"
    template = TEMPLATES["meeting-notes"]
    device = DEVICES["paper-pro-move"]
    svg, _ = render_svg(template, device)
    svg_to_png(svg, actual, device.width, device.height)
    ok, stats = compare_images(actual, baseline, diff=tmp_path / "visual-diff.png")
    assert ok, stats

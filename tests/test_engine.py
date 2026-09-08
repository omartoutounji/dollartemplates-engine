import pytest
from dollartemplates.devices.registry import DEVICES
from dollartemplates.templates.registry import TEMPLATES
from dollartemplates.renderers import render_svg
from dollartemplates.validators import validate_template, validate_layout

def test_devices_contracts():
    assert (DEVICES["paper-pro-move"].width,DEVICES["paper-pro-move"].height,DEVICES["paper-pro-move"].ppi)==(954,1696,264)
    assert (DEVICES["remarkable-2"].width,DEVICES["remarkable-2"].height,DEVICES["remarkable-2"].ppi)==(1404,1872,226)

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
    assert [s.label for s in TEMPLATES["soap-note"].sections[-4:]]==["SUBJECTIVE","OBJECTIVE","ASSESSMENT","PLAN"]

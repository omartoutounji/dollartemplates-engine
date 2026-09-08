from ..components import FieldRow, WritingArea
from ..models import Template

soap_note = Template(
    id="soap-note", title="SOAP NOTE",
    purpose="Capture a concise Subjective, Objective, Assessment, and Plan note with generous handwriting space.",
    supported_devices=["paper-pro-move", "remarkable-2"],
    layout="quadrant",
    sections=[
        FieldRow(["Date"], id="date", label="DATE"),
        WritingArea("Subjective", size="xxlarge", lines=10),
        WritingArea("Objective", size="xxlarge", lines=10),
        WritingArea("Assessment", size="xxlarge", lines=10),
        WritingArea("Plan", size="xxlarge", lines=10),
    ],
)

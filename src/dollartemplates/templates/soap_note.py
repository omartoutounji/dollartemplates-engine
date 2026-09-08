from ..components import FieldRow, WritingArea
from ..models import Template

soap_note = Template(
    id="soap-note", title="SOAP NOTE",
    purpose="Capture a concise Subjective, Objective, Assessment, and Plan note with generous handwriting space.",
    supported_devices=["paper-pro-move", "remarkable-2"],
    sections=[
        FieldRow(["Client", "Date"], id="client-date", label="SESSION"),
        FieldRow(["Provider", "Session"], id="provider-session", label="DETAILS"),
        WritingArea("Subjective", size="large", lines=5),
        WritingArea("Objective", size="medium", lines=4),
        WritingArea("Assessment", size="medium", lines=4),
        WritingArea("Plan", size="large", lines=6, expandable=True),
    ],
)

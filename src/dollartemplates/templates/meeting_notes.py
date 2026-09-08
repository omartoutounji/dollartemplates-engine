from ..components import FieldRow, WritingArea, ActionItems
from ..models import Template

meeting_notes = Template(
    id="meeting-notes", title="MEETING NOTES",
    purpose="Capture context, agenda, decisions, actions, and notes without clutter.",
    supported_devices=["paper-pro-move", "remarkable-2"],
    sections=[
        FieldRow(["Meeting", "Date"], id="meeting", label="DETAILS"),
        FieldRow(["Attendees", "Purpose"], id="people", label="PEOPLE"),
        WritingArea("Agenda", size="large", lines=4),
        WritingArea("Decisions", size="large", lines=5),
        ActionItems(rows=4),
        WritingArea("Notes", size="large", lines=8, expandable=True),
    ],
)

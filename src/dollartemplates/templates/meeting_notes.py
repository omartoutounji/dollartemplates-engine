from ..components import FieldRow, Checklist, WritingArea, ActionItems
from ..models import Template

meeting_notes = Template(
    id="meeting-notes", title="MEETING NOTES",
    purpose="Capture context, agenda, decisions, actions, and notes without clutter.",
    supported_devices=["paper-pro-move", "remarkable-2"],
    sections=[
        FieldRow(["Meeting", "Date"], id="meeting", label="MEETING"),
        FieldRow(["Attendees", "Purpose"], id="people", label="PEOPLE"),
        Checklist("Agenda", items=3),
        WritingArea("Decisions", size="small"),
        ActionItems(rows=3),
        WritingArea("Notes", size="large", expandable=True),
    ],
)

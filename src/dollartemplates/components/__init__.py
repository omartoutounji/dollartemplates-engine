import re
from ..models import FieldRowSection, ChecklistSection, WritingAreaSection, ActionItemsSection, Size

def _slug(value: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))

def FieldRow(fields: list[str], *, id: str | None = None, label: str = "DETAILS") -> FieldRowSection:
    return FieldRowSection(id=id or _slug("-".join(fields)), label=label.upper(), fields=fields)

def Checklist(label: str, *, id: str | None = None, items: int = 3) -> ChecklistSection:
    return ChecklistSection(id=id or _slug(label), label=label.upper(), items=items)

def WritingArea(label: str, *, id: str | None = None, size: Size = "medium", lines: int | None = None, expandable: bool = False) -> WritingAreaSection:
    return WritingAreaSection(id=id or _slug(label), label=label.upper(), size=size, lines=lines, expandable=expandable)

def ActionItems(*, id: str = "action-items", label: str = "ACTION ITEMS", rows: int = 3, columns: list[str] | None = None) -> ActionItemsSection:
    return ActionItemsSection(id=id, label=label.upper(), rows=rows, columns=columns or ["Task", "Owner", "Due"])

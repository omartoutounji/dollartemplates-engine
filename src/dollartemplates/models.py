from __future__ import annotations
from typing import Literal, Union
from pydantic import BaseModel, Field, model_validator

Size = Literal["small", "medium", "large"]

class SafeArea(BaseModel):
    top: int = Field(ge=0)
    right: int = Field(ge=0)
    bottom: int = Field(ge=0)
    left: int = Field(ge=0)

class Display(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    ppi: int = Field(gt=0)
    color: bool = False

class Capabilities(BaseModel):
    svg: bool = True
    png: bool = True
    pdf: bool = True
    color: bool = False

class Device(BaseModel):
    id: str
    brand: str
    name: str
    display: Display
    safe_area: SafeArea
    capabilities: Capabilities = Capabilities()
    @property
    def width(self): return self.display.width
    @property
    def height(self): return self.display.height
    @property
    def ppi(self): return self.display.ppi

class FieldRowSection(BaseModel):
    id: str
    kind: Literal["field-row"] = "field-row"
    label: str = "DETAILS"
    fields: list[str]

class ChecklistSection(BaseModel):
    id: str
    kind: Literal["checklist"] = "checklist"
    label: str
    items: int = Field(default=3, ge=1)

class WritingAreaSection(BaseModel):
    id: str
    kind: Literal["writing-area"] = "writing-area"
    label: str
    size: Size = "medium"
    lines: int | None = Field(default=None, ge=1)
    expandable: bool = False

class ActionItemsSection(BaseModel):
    id: str = "action-items"
    kind: Literal["action-items"] = "action-items"
    label: str = "ACTION ITEMS"
    rows: int = Field(default=3, ge=1)
    columns: list[str] = Field(default_factory=lambda: ["Task", "Owner", "Due"])

Section = Union[FieldRowSection, ChecklistSection, WritingAreaSection, ActionItemsSection]

class Template(BaseModel):
    id: str
    title: str
    purpose: str = ""
    supported_devices: list[str]
    sections: list[Section]
    @model_validator(mode="after")
    def structural_rules(self):
        ids = [s.id for s in self.sections]
        if len(ids) != len(set(ids)):
            raise ValueError("Section IDs must be unique.")
        return self

class Bounds(BaseModel):
    x: float
    y: float
    width: float
    height: float
    role: str

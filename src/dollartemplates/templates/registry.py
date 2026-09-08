from .meeting_notes import meeting_notes
from .soap_note import soap_note

TEMPLATES = {t.id: t for t in [meeting_notes, soap_note]}

def get_template(template_id: str):
    if template_id not in TEMPLATES:
        raise KeyError(f"Unknown template {template_id!r}. Available: {', '.join(TEMPLATES)}")
    return TEMPLATES[template_id]

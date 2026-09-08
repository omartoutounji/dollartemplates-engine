def validate_template(template, devices):
    errors=[]; warnings=[]
    for device_id in template.supported_devices:
        if device_id not in devices: errors.append(f"Unknown supported device: {device_id}")
    if len(template.sections)>7: warnings.append("Focused rule: more than 7 sections.")
    expandable=[s for s in template.sections if getattr(s,"expandable",False)]
    if len(expandable)>1: warnings.append("More than one expandable section may dilute focus.")
    if len(expandable)==1 and template.sections[-1].id != expandable[0].id: warnings.append("Expandable writing area should usually be final for e-ink workflows.")
    return errors,warnings

def _overlaps(a,b):
    return not (a.x+a.width<=b.x or b.x+b.width<=a.x or a.y+a.height<=b.y or b.y+b.height<=a.y)

def validate_layout(bounds, device):
    errors=[]; warnings=[]
    safe=(device.safe_area.left,device.safe_area.top,device.width-device.safe_area.right,device.height-device.safe_area.bottom)
    for b in bounds:
        if b.x<safe[0] or b.y<safe[1] or b.x+b.width>safe[2] or b.y+b.height>safe[3]: errors.append(f"{b.role} leaves the device safe area.")
    for i,a in enumerate(bounds):
        for b in bounds[i+1:]:
            if _overlaps(a,b): errors.append(f"Overlap: {a.role} ↔ {b.role}")
    return errors,warnings

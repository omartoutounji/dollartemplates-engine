from dataclasses import replace
from html import escape
from ..models import Bounds
from ..tokens import TOKENS

def _line(x1,y1,x2,y2,opacity=1,width=1.35):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{width}" opacity="{opacity}"/>'

def _text(x,y,value,size,weight=500,spacing=0,anchor="start"):
    return f'<text x="{x}" y="{y}" fill="#111" font-family="DejaVu Sans" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}">{escape(str(value))}</text>'

def _resolve_tokens(device, t=TOKENS):
    if not device.layout_overrides:
        return t
    overrides = dict(device.layout_overrides)
    sizes = dict(t.sizes)
    label_sizes = dict(t.label_sizes)
    if "sizes" in overrides:
        configured_sizes = overrides["sizes"]
        if isinstance(configured_sizes, dict):
            sizes.update(configured_sizes)
        overrides["sizes"] = sizes
    if "label_sizes" in overrides:
        configured_label_sizes = overrides["label_sizes"]
        if isinstance(configured_label_sizes, dict):
            label_sizes.update(configured_label_sizes)
        overrides["label_sizes"] = label_sizes
    return replace(t, **overrides)


def _section_label_size(section, t):
    if getattr(section, "kind", None) == "writing-area":
        return t.label_sizes.get(getattr(section, "size", "medium"), t.label_size)
    return t.label_size


def _section_label_spacing(section, t):
    label_size = _section_label_size(section, t)
    return max(22, int(label_size * 1.8))


def _render_region(region, area_x, area_y, area_w, area_h, t):
    parts = []
    if region.title:
        parts.append(_text(area_x, area_y + 10, region.title.upper(), t.small_label_size, 700, 1.0))
    title_end = area_y + 22

    style = region.style

    if style.kind == "ruled":
        n = style.lines or max(1, int((area_h - 22) / max(1, t.line_spacing // 2)))
        line_height = (area_h - 22) / max(n, 1)
        for i in range(n):
            ly = title_end + (i + 1) * line_height
            parts.append(_line(area_x, ly, area_x + area_w, ly, t.light_rule_opacity, 1))
    elif style.kind == "grid":
        n = style.lines or max(1, int((area_h - 22) / max(1, t.line_spacing // 2)))
        line_height = (area_h - 22) / max(n, 1)
        for i in range(n):
            ly = title_end + (i + 1) * line_height
            parts.append(_line(area_x, ly, area_x + area_w, ly, t.light_rule_opacity, 1))
        for i in range(1, 4):
            vx = area_x + i * area_w / 4
            parts.append(_line(vx, area_y, vx, area_y + area_h, t.light_rule_opacity, 1))
    elif style.kind == "dots":
        for x in range(0, int(area_w), 18):
            for y in range(0, int(area_h - 20), 18):
                cx = area_x + x + 8
                cy = area_y + 24 + y + 8
                parts.append(f'<circle cx="{cx}" cy="{cy}" r="1.2" fill="#111"/>')
    elif style.kind == "checkbox":
        for i in range(style.lines or 4):
            cy = area_y + 20 + i * (max(16, t.line_spacing // 2))
            parts.append(f'<rect x="{area_x}" y="{cy - 8}" width="{t.checkbox_size}" height="{t.checkbox_size}" fill="none" stroke="#111" stroke-width="{t.rule_width}"/>')
            parts.append(_line(area_x + t.checkbox_size + 16, cy + 2, area_x + area_w, cy + 2, t.light_rule_opacity, 1))
    elif style.kind == "table":
        parts.append(f'<rect x="{area_x}" y="{area_y}" width="{area_w}" height="{area_h}" fill="none" stroke="#111" stroke-width="{t.rule_width}"/>')
        row_h = area_h / max(1, style.rows or 3)
        for i in range(1, style.rows or 3):
            parts.append(_line(area_x, area_y + i * row_h, area_x + area_w, area_y + i * row_h, t.light_rule_opacity, 1))
    return parts


def _render_page(template, device, t):
    left=device.safe_area.left+t.page_padding; right=device.width-device.safe_area.right-t.page_padding
    content_w=right-left; parts=[]; bounds=[]; y=device.safe_area.top+t.page_padding
    parts += [f'<svg xmlns="http://www.w3.org/2000/svg" width="{device.width}" height="{device.height}" viewBox="0 0 {device.width} {device.height}">','<rect width="100%" height="100%" fill="#fff"/>']
    if template.show_page_title:
        parts.append(_text(left,y+t.heading_size,template.title,t.heading_size,700,1.2))
        parts.append(_text(right,y+t.heading_size-2,"DOLLARTEMPLATES",10,500,2.0,"end")); y += t.heading_size+32
    else:
        y += 8

    if template.page.layout == "quadrants":
        footer_height = 28
        body_top = y + 8
        body_bottom = device.height - device.safe_area.bottom - footer_height
        body_h = body_bottom - body_top
        quad_w = content_w / 2
        quad_h = body_h / 2

        for idx, region in enumerate(template.page.regions):
            row = idx // 2
            col = idx % 2
            area_x = left + col * quad_w + 6
            area_y = body_top + row * quad_h + 6
            area_w = quad_w - 12
            area_h = quad_h - 12
            parts.extend(_render_region(region, area_x, area_y, area_w, area_h, t))
            bounds.append(Bounds(x=area_x, y=area_y, width=area_w, height=area_h, role=region.id))

        parts.append(_line(left + quad_w, body_top, left + quad_w, body_bottom, 0.8, 1))
        parts.append(_line(left, body_top + quad_h, right, body_top + quad_h, 0.8, 1))

    else:
        for region in template.page.regions:
            region_y = y
            region_h = max(120, (device.height - device.safe_area.bottom - region_y - 40) / max(1, len(template.page.regions)))
            parts.extend(_render_region(region, left, region_y, content_w, region_h, t))
            bounds.append(Bounds(x=left, y=region_y, width=content_w, height=region_h, role=region.id))
            y += region_h + t.section_gap

    footer_y=device.height-device.safe_area.bottom-18
    parts.append(_text(left,footer_y,"MINIMAL · INTENTIONAL · FOCUSED",9,500,1.3))
    bounds.append(Bounds(x=left,y=footer_y-12,width=content_w,height=16,role="footer")); parts.append('</svg>')
    return "\n".join(parts), bounds


def render_svg(template, device, t=TOKENS):
    t = _resolve_tokens(device, t)
    if template.page:
        return _render_page(template, device, t)

    left=device.safe_area.left+t.page_padding; right=device.width-device.safe_area.right-t.page_padding
    content_w=right-left; parts=[]; bounds=[]; y=device.safe_area.top+t.page_padding
    parts += [f'<svg xmlns="http://www.w3.org/2000/svg" width="{device.width}" height="{device.height}" viewBox="0 0 {device.width} {device.height}">','<rect width="100%" height="100%" fill="#fff"/>']
    if template.show_page_title:
        parts.append(_text(left,y+t.heading_size,template.title,t.heading_size,700,1.2))
        parts.append(_text(right,y+t.heading_size-2,"DOLLARTEMPLATES",10,500,2.0,"end")); y += t.heading_size+32
    else:
        y += 8
    if template.layout == "quadrant":
        top_margin = 8
        footer_height = 28
        body_top = y + top_margin
        body_bottom = device.height - device.safe_area.bottom - footer_height
        body_h = body_bottom - body_top
        quad_w = content_w / 2
        quad_h = body_h / 2

        parts.append(_text(right, y, "Date ____ / ____ / ____", t.small_label_size, 600, 1.0, "end"))

        parts.append(_line(left + quad_w, body_top, left + quad_w, body_bottom, 0.8, 1))
        parts.append(_line(left, body_top + quad_h, right, body_top + quad_h, 0.8, 1))

        for idx, section in enumerate(template.sections[1:]):
            if section.kind != "writing-area":
                continue
            row = idx // 2
            col = idx % 2
            area_x = left + col * quad_w + 6
            area_y = body_top + row * quad_h + 6
            area_w = quad_w - 12
            area_h = quad_h - 12
            label_size = _section_label_size(section, t)
            label_spacing = _section_label_spacing(section, t)
            parts.append(_text(area_x, area_y + label_size, section.label.upper(), label_size, 700, 1.0))
            n = section.lines or t.sizes[section.size]
            line_height = (area_h - label_spacing) / max(n, 1)
            for i in range(n):
                ly = area_y + label_spacing + (i + 1) * line_height
                parts.append(_line(area_x, ly, area_x + area_w, ly, t.light_rule_opacity, 1))
            bounds.append(Bounds(x=area_x, y=area_y, width=area_w, height=area_h, role=section.id))
        footer_y=device.height-device.safe_area.bottom-18
        parts.append(_text(left,footer_y,"MINIMAL · INTENTIONAL · FOCUSED",9,500,1.3))
        bounds.append(Bounds(x=left,y=footer_y-12,width=content_w,height=16,role="footer")); parts.append('</svg>')
        return "\n".join(parts), bounds

    for section in template.sections:
        section_top=y-t.label_size; parts.append(_text(left,y,section.label,_section_label_size(section, t),700,1.5)); y+=18
        if section.kind=="field-row":
            gap=24; width=(content_w-gap*(len(section.fields)-1))/len(section.fields)
            for i,field in enumerate(section.fields):
                x=left+i*(width+gap); parts.append(_text(x,y+14,field.upper(),t.small_label_size,600,1.1)); parts.append(_line(x,y+42,x+width,y+42,.72,t.rule_width))
            y+=50
        elif section.kind=="checklist":
            for i in range(section.items):
                cy=y+20+i*t.line_spacing; parts.append(f'<rect x="{left}" y="{cy-t.checkbox_size+2}" width="{t.checkbox_size}" height="{t.checkbox_size}" fill="none" stroke="#111" stroke-width="{t.rule_width}"/>'); parts.append(_line(left+t.checkbox_size+16,cy+2,right,cy+2,t.light_rule_opacity,1))
            y+=section.items*t.line_spacing+8
        elif section.kind=="writing-area":
            n=section.lines or t.sizes[section.size]
            label_size = _section_label_size(section, t)
            label_spacing = _section_label_spacing(section, t)
            parts.append(_text(left, y, section.label, label_size, 700, 1.5))
            box_top = y + label_spacing
            box_height=max(120, n*t.line_spacing + label_spacing + 12)
            parts.append(f'<rect x="{left}" y="{box_top}" width="{content_w}" height="{box_height}" fill="none" stroke="#111" stroke-width="{t.rule_width}"/>')
            for i in range(n):
                ly=box_top+18+i*t.line_spacing; parts.append(_line(left+2,ly,right-2,ly,t.light_rule_opacity,1))
            y += box_height + label_spacing + 8
        elif section.kind=="action-items":
            task_w=content_w*.62; owner_w=content_w*.20; xs=[left,left+task_w,left+task_w+owner_w,right]
            row_height=max(52, 28 + section.rows*8)
            for i,label in enumerate(section.columns): parts.append(_text(xs[i]+6,y+14,label.upper(),t.small_label_size,600,1.0))
            y+=26
            for r in range(section.rows+1): parts.append(_line(left,y+r*row_height,right,y+r*row_height,.45,1))
            for x in xs: parts.append(_line(x,y,x,y+section.rows*row_height,.45,1))
            y+=section.rows*row_height
        bounds.append(Bounds(x=left,y=section_top,width=content_w,height=y-section_top,role=section.id)); y+=t.section_gap
    footer_y=device.height-device.safe_area.bottom-18
    parts.append(_text(left,footer_y,"MINIMAL · INTENTIONAL · FOCUSED",9,500,1.3))
    bounds.append(Bounds(x=left,y=footer_y-12,width=content_w,height=16,role="footer")); parts.append('</svg>')
    return "\n".join(parts), bounds

from html import escape
from ..models import Bounds
from ..tokens import TOKENS

def _line(x1,y1,x2,y2,opacity=1,width=1.35):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{width}" opacity="{opacity}"/>'

def _text(x,y,value,size,weight=500,spacing=0,anchor="start"):
    return f'<text x="{x}" y="{y}" fill="#111" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}">{escape(str(value))}</text>'

def render_svg(template, device, t=TOKENS):
    left=device.safe_area.left+t.page_padding; right=device.width-device.safe_area.right-t.page_padding
    content_w=right-left; parts=[]; bounds=[]; y=device.safe_area.top+t.page_padding
    parts += [f'<svg xmlns="http://www.w3.org/2000/svg" width="{device.width}" height="{device.height}" viewBox="0 0 {device.width} {device.height}">','<rect width="100%" height="100%" fill="#fff"/>']
    parts.append(_text(left,y+t.heading_size,template.title,t.heading_size,700,1.2))
    parts.append(_text(right,y+t.heading_size-2,"DOLLARTEMPLATES",10,500,2.0,"end")); y += t.heading_size+32
    for section in template.sections:
        section_top=y-t.label_size; parts.append(_text(left,y,section.label,t.label_size,700,1.5)); y+=18
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
            for i in range(n):
                ly=y+22+i*t.line_spacing; parts.append(_line(left,ly,right,ly,t.light_rule_opacity,1))
            y+=n*t.line_spacing+4
        elif section.kind=="action-items":
            task_w=content_w*.62; owner_w=content_w*.20; xs=[left,left+task_w,left+task_w+owner_w,right]
            for i,label in enumerate(section.columns): parts.append(_text(xs[i]+6,y+14,label.upper(),t.small_label_size,600,1.0))
            y+=26
            for r in range(section.rows+1): parts.append(_line(left,y+r*44,right,y+r*44,.45,1))
            for x in xs: parts.append(_line(x,y,x,y+section.rows*44,.45,1))
            y+=section.rows*44
        bounds.append(Bounds(x=left,y=section_top,width=content_w,height=y-section_top,role=section.id)); y+=t.section_gap
    footer_y=device.height-device.safe_area.bottom-18
    parts.append(_text(left,footer_y,"MINIMAL · INTENTIONAL · FOCUSED",9,500,1.3)); parts.append(_text(right,footer_y,f"{template.title} · 01",9,500,1.3,"end"))
    bounds.append(Bounds(x=left,y=footer_y-12,width=content_w,height=16,role="footer")); parts.append('</svg>')
    return "\n".join(parts), bounds

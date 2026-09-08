from pathlib import Path
import re
import typer
from .devices.registry import DEVICES
from .templates.registry import TEMPLATES
from .renderers import render_svg, svg_to_png, svg_to_pdf
from .validators import validate_template, validate_layout

app=typer.Typer(no_args_is_help=True,help="DollarTemplates e-ink template engine")

def _root():
    p=Path.cwd()
    while p!=p.parent:
        if (p/"pyproject.toml").exists(): return p
        p=p.parent
    return Path.cwd()

@app.command()
def devices():
    for d in DEVICES.values(): typer.echo(f"{d.id:18} {d.name}  {d.width}x{d.height} @ {d.ppi}ppi")

@app.command()
def templates():
    for t in TEMPLATES.values(): typer.echo(f"{t.id:18} {t.title}  [{', '.join(t.supported_devices)}]")

@app.command("new")
def new_template(name:str):
    slug=re.sub(r"[^a-z0-9]+","-",name.lower()).strip("-"); var=slug.replace("-","_"); path=_root()/"src"/"dollartemplates"/"templates"/f"{var}.py"
    if path.exists(): raise typer.BadParameter(f"Already exists: {path}")
    title=slug.replace("-"," ").upper()
    content = "from ..components import FieldRow, WritingArea\nfrom ..models import Template\n\n"
    content += f"{var} = Template(\n    id={slug!r},\n    title={title!r},\n    supported_devices=['paper-pro-move'],\n    sections=[\n        FieldRow(['Title', 'Date']),\n        WritingArea('Notes', size='large', expandable=True),\n    ],\n)\n"
    path.write_text(content); typer.echo(f"Created {path}"); typer.echo(f"Add {var} to templates/registry.py")

@app.command()
def build(template_id:str, device:list[str]=typer.Option(None,"--device"), all_devices:bool=typer.Option(False,"--all"), pdf:bool=False, svg_only:bool=False):
    if template_id not in TEMPLATES: raise typer.BadParameter(f"Unknown template. Available: {', '.join(TEMPLATES)}")
    template=TEMPLATES[template_id]; requested=template.supported_devices if all_devices or not device else device
    errors,warnings=validate_template(template,DEVICES)
    for w in warnings: typer.echo(f"WARN {w}")
    if errors:
        for e in errors: typer.echo(f"FAIL {e}")
        raise typer.Exit(1)
    for did in requested:
        if did not in template.supported_devices: raise typer.BadParameter(f"{template_id} does not declare support for {did}")
        if did not in DEVICES: raise typer.BadParameter(f"Unknown device: {did}")
        d=DEVICES[did]; svg,bounds=render_svg(template,d); layout_errors,_=validate_layout(bounds,d)
        if layout_errors:
            for e in layout_errors: typer.echo(f"FAIL {did}: {e}")
            raise typer.Exit(1)
        out=_root()/"output"/template.id/did; out.mkdir(parents=True,exist_ok=True); svg_path=out/f"{template.id}.svg"; svg_path.write_text(svg)
        if not svg_only: svg_to_png(svg,out/f"{template.id}.png",d.width,d.height)
        if pdf: svg_to_pdf(svg,out/f"{template.id}.pdf")
        typer.echo(f"PASS {template.id} -> {did} ({d.width}x{d.height})")
        typer.echo(f"  {out}")


if __name__ == "__main__":
    app()

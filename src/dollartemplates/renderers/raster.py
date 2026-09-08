from pathlib import Path
import cairosvg

def svg_to_png(svg: str, output: Path, width: int, height: int):
    output.parent.mkdir(parents=True,exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(output),output_width=width,output_height=height)

def svg_to_pdf(svg: str, output: Path):
    output.parent.mkdir(parents=True,exist_ok=True)
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(output))

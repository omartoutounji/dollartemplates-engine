from ...models import Device, Display, SafeArea, Capabilities

paper_pro_move = Device(
    id="paper-pro-move", brand="remarkable", name="reMarkable Paper Pro Move",
    display=Display(width=954, height=1696, ppi=264, color=True),
    safe_area=SafeArea(top=48, right=42, bottom=40, left=42),
    capabilities=Capabilities(svg=True, png=True, pdf=True, color=True),
)

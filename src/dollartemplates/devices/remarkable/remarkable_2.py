from ...models import Device, Display, SafeArea, Capabilities

remarkable_2 = Device(
    id="remarkable-2", brand="remarkable", name="reMarkable 2",
    display=Display(width=1404, height=1872, ppi=226, color=False),
    safe_area=SafeArea(top=48, right=42, bottom=40, left=42),
    capabilities=Capabilities(svg=True, png=True, pdf=True, color=False),
)

from ...models import Device, Display, SafeArea, Capabilities

remarkable_2 = Device(
    id="remarkable-2", brand="remarkable", name="reMarkable 2",
    display=Display(width=1404, height=1872, ppi=226, color=False),
    safe_area=SafeArea(top=48, right=42, bottom=40, left=42),
    capabilities=Capabilities(svg=True, png=True, pdf=True, color=False),
    layout_overrides={
        "page_padding": 36,
        "section_gap": 18,
        "heading_size": 30,
        "label_size": 13,
        "small_label_size": 9,
        "line_spacing": 32,
        "checkbox_size": 15,
        "sizes": {"small": 2, "medium": 4, "large": 6},
        "label_sizes": {"small": 10, "medium": 12, "large": 14, "xlarge": 18, "xxlarge": 22},
    },
)

from dataclasses import dataclass, field

@dataclass(frozen=True)
class DesignTokens:
    page_padding: int = 42
    section_gap: int = 22
    heading_size: int = 34
    label_size: int = 14
    small_label_size: int = 10
    rule_width: float = 1.35
    light_rule_opacity: float = 0.30
    line_spacing: int = 38
    checkbox_size: int = 17
    sizes: dict[str, int] = field(default_factory=lambda: {"small": 3, "medium": 5, "large": 8})
    label_sizes: dict[str, int] = field(default_factory=lambda: {"small": 11, "medium": 13, "large": 16, "xlarge": 20, "xxlarge": 24})

TOKENS = DesignTokens()

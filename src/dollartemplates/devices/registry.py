from .remarkable.paper_pro_move import paper_pro_move
from .remarkable.remarkable_2 import remarkable_2

DEVICES = {d.id: d for d in [paper_pro_move, remarkable_2]}
DEVICE_GROUPS = {"remarkable": list(DEVICES)}

def get_device(device_id: str):
    if device_id not in DEVICES:
        raise KeyError(f"Unknown device {device_id!r}. Available: {', '.join(DEVICES)}")
    return DEVICES[device_id]

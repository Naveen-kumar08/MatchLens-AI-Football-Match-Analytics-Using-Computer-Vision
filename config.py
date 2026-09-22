from dataclasses import dataclass
import yaml

@dataclass
class Config:
    model: str
    confidence: float
    iou: float
    device: str
    imgsz: int
    pitch_length: float
    pitch_width: float
    image_points: list
    tactical_width: int
    tactical_height: int
    fps: float

    @classmethod
    def from_yaml(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            d = yaml.safe_load(f)

        p = d["pitch"]
        o = d["output"]

        return cls(
            model=d["model"],
            confidence=float(d["confidence"]),
            iou=float(d["iou"]),
            device=d.get("device", "auto"),
            imgsz=int(d.get("imgsz", 1280)),
            pitch_length=float(p["length_m"]),
            pitch_width=float(p["width_m"]),
            image_points=p["image_points"],
            tactical_width=int(o["tactical_width"]),
            tactical_height=int(o["tactical_height"]),
            fps=float(o.get("fps", 25)),
        )

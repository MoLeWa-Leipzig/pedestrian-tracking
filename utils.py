from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Point():
    x: float
    y: float
    z: Optional[float] 

@dataclass
class TrackPoint():
    point: Point 
    prob: float 
    track_id: str 
    class_id: str
    ts: datetime.datetime
    frame_nr: int

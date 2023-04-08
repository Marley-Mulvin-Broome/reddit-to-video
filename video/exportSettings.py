from enum import Enum
from dataclasses import dataclass


class Compression(Enum):
    UltraFast: str = "ultrafast"
    SuperFast: str = "superfast"
    VeryFast: str = "veryfast"
    Faster: str = "faster"
    Fast: str = "fast"
    Medium: str = "medium"
    Slow: str = "slow"
    Slower: str = "slower"
    VerySlow: str = "veryslow"
    Placebo: str = "placebo"


@dataclass
class ExportSettings:
    codec: str = "libx264"
    bitrate: str = "5000k"

    compression: Compression = Compression.SuperFast

    fps: int = 30
    threads: int = 4

    def unbox(self) -> dict:
        return {
            "codec": self.codec,
            "bitrate": self.bitrate,
            "compression": self.compression.value,
            "fps": self.fps,
            "threads": self.threads
        }

from enum import Enum
from dataclasses import dataclass


class Compression(Enum):
    """Compression presets for ffmpeg"""
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
    """Export settings for videos"""
    codec: str = "libx264"
    bitrate: str = "5000k"

    compression: str = Compression.SuperFast.value

    fps: int = 30
    threads: int = 4

    def unbox(self) -> dict:
        return {
            "codec": self.codec,
            "bitrate": self.bitrate,
            "preset": self.compression,
            "fps": self.fps,
            "threads": self.threads
        }

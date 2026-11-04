"""数据模型.

定义脉搏数据的数据模型。
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class PulseChannel:
    """脉搏通道."""
    position: str
    waveform: np.ndarray

    def __post_init__(self):
        if not isinstance(self.waveform, np.ndarray):
            self.waveform = np.array(self.waveform)


@dataclass
class PulseSource:
    """脉搏源."""
    patient_id: str
    device_id: str
    acquisition_time: str
    checksum: Dict[str, str]


@dataclass
class PulseInput:
    """脉搏输入."""
    source: PulseSource
    channels: Dict[str, PulseChannel]


@dataclass
class PulseOutput:
    """脉搏输出."""
    diagnosis: str
    confidence: float
    details: Dict[str, Any]

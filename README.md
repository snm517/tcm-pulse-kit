# TCM Pulse Kit

> 中医脉象分析工具包 v0.2.0

## 概述

TCM Pulse Kit 是一个用于中医脉象分析的工具包，支持六部脉象（左寸、左关、左尺、右寸、右关、右尺）的特征提取、相对值分析、十变推理和五行拓扑引擎。

## 功能特性

- **信号预处理**: 带通滤波、基线漂移校正、分段（浮取/沉取）
- **周期特征提取**: 峰值幅度、上升时间、下降时间、FWHM、面积、脉长
- **相对值分析**: 六部内部z-score标准化、Winsorization缩尾处理
- **十变推理**: 急、大、缓、涩、沉五态及浮沉比判定
- **五行拓扑引擎**: 完整的生克乘侮关系分析、病机传变路径搜索
- **质量门禁**: SNR评估、连续性检查、标准差检查

## 快速开始

### 安装

```bash
pip install -e .
```

### 使用示例

```python
import numpy as np
from tcm_pulse_kit import PulseDiagnosisPipeline
from tcm_pulse_kit.io.schema import PulseInput, PulseChannel, PulseSource

# 创建模拟信号
fs = 1000
t = np.arange(0, 10, 1/fs)
channels = {}
for pos in ["左寸", "左关", "左尺", "右寸", "右关", "右尺"]:
    waveform = np.sin(2 * np.pi * 1.2 * t)
    channels[pos] = PulseChannel(position=pos, waveform=waveform)

source = PulseSource(
    patient_id="TEST_001",
    device_id="SIMULATOR",
    acquisition_time="2026-10-28T07:00:00",
    checksum={},
)
pulse_input = PulseInput(source=source, channels=channels)

# 运行诊断
pipeline = PulseDiagnosisPipeline(fs=fs)
report = pipeline.run(pulse_input)

print(f"置信度: {report.overall_confidence}")
print(f"十变结果: {len(report.shibian)}")
```

## 五行分析

```python
from tcm_pulse_kit.wuxing import (
    WuxingTopologyEngine,
    WuxingIntegratedDiagnosis,
    DetailedElementMapper,
)

# 创建五行引擎
element_mapper = DetailedElementMapper()
wuxing_engine = WuxingTopologyEngine()
wuxing_diagnosis = WuxingIntegratedDiagnosis(element_mapper, wuxing_engine)

# 增强诊断报告
enhanced_report = wuxing_diagnosis.enhance_diagnosis(report, analysis_input)
```

## 项目结构

```
tcm-pulse-kit/
├── src/tcm_pulse_kit/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── core/
│   │   ├── preprocessor.py
│   │   ├── feature_extractor.py
│   │   ├── relative_engine.py
│   │   ├── shibian_engine.py
│   │   └── quality_gate.py
│   ├── wuxing/
│   │   ├── __init__.py
│   │   ├── topology_engine.py
│   │   ├── integration.py
│   │   ├── data_flow.py
│   │   ├── element_mapping.py
│   │   ├── architecture.py
│   │   ├── structured_output.py
│   │   └── data_scale.py
│   ├── io/
│   └── diagnosis/
├── knowledge/
│   └── wutai_weights.yaml
├── tests/
└── README.md
```

## 版本历史

- **v0.2.0** (2026-10-28)
  - 新增五行拓扑引擎
  - 修复26个对抗性审查发现的问题
  - 优化系统架构
  - 添加完整测试套件

## 许可证

MIT License

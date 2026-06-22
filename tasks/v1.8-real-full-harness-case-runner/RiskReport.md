# RiskReport — v1.8 harness case runner

## 风险等级
- [x] 低

## 风险
| Risk | Impact | Handling |
|:---|:---|:---|
| Python version incompatibility | runner may fail on Python 2 | documented requirement: Python 3 |
| Windows path separator | subprocess uses sys.executable pattern | test on Windows passes |

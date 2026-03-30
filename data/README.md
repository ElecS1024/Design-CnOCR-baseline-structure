# 数据目录说明

本目录存放当前项目使用的全部数据与标签文件。

## 目录用途

- `raw/`：原始数据，保留 LMDB 等原始格式，不直接参与 baseline 推理
- `processed/`：处理中间产物，例如从完整测试集切出的特殊子集
- `sample/`：用于快速跑通 baseline 的小样本图片目录
- `train/`：训练集图片目录
- `val/`：验证集图片目录
- `test/`：测试集图片目录

## 标签文件说明

- `labels_sample.csv`：`sample/` 的标签文件
- `labels_train.csv`：`train/` 的标签文件
- `labels_val.csv`：`val/` 的标签文件
- `labels_test.csv`：`test/` 的标签文件
- `labels_hard_cases.csv`：从完整测试集里单独抽取出的困难样本子集标签

## 查看建议

- 想快速看项目是否能跑通，先看 `sample/`
- 想看正式训练和测试数据，重点看 `train/`、`val/`、`test/`
- 想看原始来源和类别划分，重点看 `raw/mindocr_chinese_text_recognition/`
- 想看困难样本子集，重点看 `processed/hard_cases_eval/`

# 2026-03-17 工作总结

## 今天完成了什么

### 1. 项目环境搭建与修正

- 创建并确认 `cnocr` conda 环境
- 安装项目依赖，包括 `cnocr`、`torch`、`opencv-python`、`pillow`、`onnxruntime`、`lmdb`
- 运行环境检查脚本 [01_check_env.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/01_check_env.py)
- 修正 CnOCR 默认模型配置问题，使脚本兼容当前 `cnocr 2.3.2.3`

### 2. 数据集整理与导入

- 将 MindOCR/Fudan 中文识别整理集按正式目录归档到：
  - `data/raw/mindocr_chinese_text_recognition/training`
  - `data/raw/mindocr_chinese_text_recognition/validation`
  - `data/raw/mindocr_chinese_text_recognition/evaluation`
- 将 `Hard-Cases` 困难样本单独整理到 `evaluation` 路径下
- 新增 LMDB 导入脚本 [06_import_mindocr_lmdb.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/06_import_mindocr_lmdb.py)
- 完成图片与标签导出，生成：
  - `data/train`
  - `data/val`
  - `data/test`
  - `data/sample`
  - `labels_train.csv`
  - `labels_val.csv`
  - `labels_test.csv`
  - `labels_sample.csv`

### 3. Baseline 流程跑通

- 在 `sample` 数据上运行 baseline 推理
- 生成预测结果文件 [baseline_preds.csv](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/preds/baseline_preds.csv)
- 运行整体评测脚本 [03_eval_baseline.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/03_eval_baseline.py)
- 生成 baseline 指标文件 [baseline_metrics.json](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/baseline_metrics.json)
- 运行案例可视化脚本 [05_visualize_cases.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/05_visualize_cases.py)

### 4. 困难样本与完整测试集实验

- 从完整测试集中抽出 `hard_cases` 子集，共 905 条
- 运行 hard cases baseline 推理与评测
- 新增分组评测脚本 [07_group_eval.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/07_group_eval.py)
- 新增总对比表脚本 [08_build_summary_table.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/08_build_summary_table.py)
- 完成完整 `test` 集 baseline 推理，共 128,610 条
- 生成：
  - [test_preds.csv](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/preds/test_preds.csv)
  - [test_metrics.json](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/test_metrics.json)
  - [test_group_metrics.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/test_group_metrics.md)
  - [summary_table.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/summary_table.md)

### 5. 文档整理

- 更新 [experiment_record.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/docs/experiment_record.md)
- 更新 [thesis_notes.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/docs/thesis_notes.md)
- 补充 baseline 与 hard cases 的论文草稿描述

## 当前核心结果

### sample baseline

- 样本数：50
- 行准确率：80.0%
- 字符准确率：95.10%
- 平均编辑距离：0.36

### hard cases

- 样本数：905
- 行准确率：17.90%
- 字符准确率：32.40%
- 平均编辑距离：2.8674

### full test

- 样本数：128,610
- 行准确率：53.50%
- 字符准确率：76.26%
- 平均编辑距离：1.4666

### 完整测试集分组结果概览

- `document`：行准确率 77.65%，字符准确率 95.48%
- `scene`：行准确率 38.13%，字符准确率 57.74%
- `web`：行准确率 39.45%，字符准确率 54.07%
- `hard_cases`：行准确率 17.90%，字符准确率 32.40%

## 接下来建议怎么做

### 第一优先级

- 结合 [test_group_metrics.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/test_group_metrics.md) 和 [summary_table.md](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/eval/summary_table.md) 撰写论文第五章实验结果部分
- 抽取 `scene / web / hard_cases` 中的典型错误案例，补充误差分析图片

### 第二优先级

- 针对 `vertical_text`、`oblique_or_curved`、`occlusion` 等困难类型设计增强或微调方案
- 保留 `document` 作为相对容易的对照组，突出 baseline 在不同场景中的性能差异

### 第三优先级

- 如果后续打算做微调，优先构建以下实验对比：
  - baseline
  - baseline + 困难样本补充
  - baseline + 有针对性微调

## 你下一次继续时最建议从哪里开始

建议直接从下面两件事之一开始：

1. 写论文：
  直接使用 `docs/thesis_notes.md`、`outputs/eval/summary_table.md`、`outputs/eval/test_group_metrics.md`
2. 做改进实验：
  优先围绕 `vertical_text` 和 `oblique_or_curved` 两类样本设计后续优化


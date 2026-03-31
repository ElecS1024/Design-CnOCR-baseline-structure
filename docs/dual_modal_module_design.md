# 双模态模块设计说明

## 设计目标

在保留现有 CnOCR baseline 结果与脚本链路不变的前提下，新增一套独立的双模态 OCR 实验模块，用于完成“视觉特征 + 文本语义特征”的改进实验，并为论文中的模型改进章节提供实现依据。

## 模块组成

### 1. 视觉主模态

- 输入：中文单行文本图像
- 编码方式：卷积特征提取 + 序列编码
- 输出：按时间步展开的视觉序列特征

### 2. 文本语义辅助模态

- 输入：字符序列
- 训练阶段：使用真实标签构建语义分支输入
- 推理阶段：使用视觉分支的初步预测构建语义分支输入
- 编码方式：字符嵌入 + 双向 GRU
- 输出：全局语义表示

### 3. 融合模块

- 融合位置：识别头之前
- 融合方式：门控融合
- 目的：根据视觉特征与语义特征的互补关系生成最终识别特征

### 4. 识别输出

- 输出形式保持与 baseline 一致
- 可直接复用现有评测脚本进行总体评测与分组评测

## 当前实现文件

- `models/dual_modal_ocr.py`
- `experiments/dual_modal/data.py`
- `experiments/dual_modal/tokenizer.py`
- `experiments/dual_modal/metrics.py`
- `scripts/09_train_dual_modal.py`
- `scripts/10_predict_dual_modal.py`

## 推荐实验流程

1. 使用 `09_train_dual_modal.py` 进行训练
2. 在验证集上确认模型收敛方向
3. 使用 `10_predict_dual_modal.py` 在 `hard_cases` 和 `test` 上输出预测结果
4. 复用 `03_eval_baseline.py` 和 `07_group_eval.py` 生成总体指标和分组指标
5. 使用 `08_build_summary_table.py` 汇总 baseline 与双模态实验结果

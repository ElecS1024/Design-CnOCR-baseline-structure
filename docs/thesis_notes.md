# Thesis Notes

## Chapter Mapping

- Chapter 3: data collection, cleaning, and dataset split strategy
- Chapter 4: hardware, software, and implementation details
- Chapter 5: baseline metrics, fine-tuning comparison, and error analysis

## Writing Reminders

- Record every experiment with exact model names and dataset versions.
- Save baseline prediction files and visualized cases for later figures.
- Keep train/val/test split rules fixed once the formal experiments begin.

## 2026-03-31 Server Training Progress

- Remote training server has been prepared successfully.
- Server profile:
  - GPU: `Tesla P100-PCIE-16GB`
  - OS: `Ubuntu 20.04`
  - Driver / CUDA: `570.195.03 / 12.8`
- All formal data splits were uploaded and extracted on the server.
- The first GPU attempt with `torch 2.9.1+cu128` failed because `P100` is `sm_60`.
- The server runtime was switched to `torch 2.9.1+cu126`, after which a dual-modal probe run completed successfully.
- Formal server-side dual-modal training has completed.
- Current formal validation result:
  - `line_acc=0.010665`
  - `char_acc=0.127606`
  - `avg_edit_distance=5.399424`
- Epoch-level trend:
  - Epoch 1: `train_loss=5.969488`, `val_line_acc=0.003093`, `val_char_acc=0.023286`
  - Epoch 2: `train_loss=3.160761`, `val_line_acc=0.010665`, `val_char_acc=0.127606`

## 2026-03-31 Dual-Modal Hard Cases Result

- Evaluation split: `hard_cases (905 images)`
- Checkpoint: `outputs/dual_modal/checkpoints/best.pt`
- Overall result:
  - `line_acc=0.002210`
  - `char_acc=0.019276`
  - `avg_edit_distance=4.160221`
- Grouped result highlights:
  - `bg_confusion`: `line_acc=0.000000`, `char_acc=0.024000`
  - `blur`: `line_acc=0.004000`, `char_acc=0.012491`
  - `oblique_or_curved`: `line_acc=0.000000`, `char_acc=0.017613`
  - `occlusion`: `line_acc=0.000000`, `char_acc=0.044964`
  - `vertical_text`: `line_acc=0.000000`, `char_acc=0.002193`

Current observation:

- the current dual-modal checkpoint is still much weaker than the baseline on `hard_cases`
- the first formal server run proves that the training path is stable, but this checkpoint is not yet strong enough to claim improvement
- for the thesis, this result should be described honestly as an early-stage formal training result rather than a final improved model

## 2026-03-31 Dual-Modal V2 Result

- Model tag: `dual_modal_v2`
- Server config:
  - GPU: `Tesla P100-PCIE-16GB`
  - torch runtime: `2.9.1+cu126`
  - epochs: `5`
  - batch_size: `16`
  - max_steps_per_epoch: `8000`

### Validation Result

- `line_acc=0.210228`
- `char_acc=0.560172`
- `avg_edit_distance=2.722186`

### Hard Cases Result

- `line_acc=0.041989`
- `char_acc=0.160719`
- `avg_edit_distance=3.560221`

### Full Test Result

- `line_acc=0.210054`
- `char_acc=0.557444`
- `avg_edit_distance=2.733979`

### Baseline Comparison Note

- `dual_modal_v2` is much stronger than the earlier short dual-modal runs.
- However, it is still below the baseline on both `hard_cases` and `full_test`.
- This means the current improved pipeline is technically stable and has meaningful training progress, but the present checkpoint still cannot be written as a final outperforming model.
- In the thesis, the most appropriate framing is:
  - the dual-modal method was successfully designed and implemented
  - server-side training and evaluation were completed
  - the current version still needs further tuning before it can surpass the baseline

### Files Ready for Thesis Use

- `outputs/eval/dual_modal_formal_train_summary.md`
- `outputs/eval/dual_modal_hard_cases_summary.md`
- `outputs/eval/dual_modal_v2_summary_table.md`
- `outputs/eval/dual_modal_v2_group_compare.md`

## 2026-03-31 Optimization Direction Update

### Why another experiment is needed

- The current `dual_modal_v2` result is still below the pretrained baseline.
- Therefore, the thesis should not directly claim that adding a dual-modal module has already improved the full system.
- A more rigorous next step is to add a `single_modal` control experiment under the same training framework.

### Controlled ablation logic

- `baseline`: pretrained CnOCR reference model
- `single_modal`: same visual encoder and CTC pipeline as the current dual-modal experiment, but without semantic branch or gated fusion
- `dual_modal`: visual branch + semantic branch + gated fusion

If the result shows `single_modal < dual_modal`, then the thesis can reasonably argue that the second modality provides positive value inside the new architecture, even if the overall system still has not exceeded the original baseline.

### Recommended thesis framing

- First, establish the baseline and identify the hard-case bottleneck.
- Second, present the dual-modal design.
- Third, add a single-modal ablation experiment.
- Finally, analyze whether the semantic branch improves the model on difficult subsets such as `vertical_text`, `oblique_or_curved`, and `occlusion`.

## Baseline Experiment Draft

### 1. Experiment Goal

本阶段实验的目标是搭建并验证中文单行文本识别 baseline 流程，确认从环境配置、数据准备、模型推理、结果评测到案例可视化的完整链路能够正常运行，为后续微调实验和论文写作提供基础支撑。

### 2. Experiment Environment

- Python: 3.10.20
- CnOCR: 2.3.2.3
- PyTorch: 2.10.0+cpu
- OpenCV: 4.13.0
- Backend: onnxruntime
- Device: CPU

可在 [01_check_env.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/01_check_env.py) 中复现实验环境检查流程。

### 3. Dataset Description

实验使用项目导入后的 sample 子集作为 baseline 初始验证数据，共 50 张中文单行文本图像。该 sample 数据由正式训练数据自动抽样生成，主要用于快速验证 baseline 推理流程和评测脚本是否正常工作。

当前项目中正式数据已整理为以下结构：

- `data/train`
- `data/val`
- `data/test`
- `data/sample`

对应标签文件为：

- `data/labels_train.csv`
- `data/labels_val.csv`
- `data/labels_test.csv`
- `data/labels_sample.csv`

### 4. Evaluation Metrics

本阶段采用以下指标对 baseline 进行评估：

- 行准确率：预测文本与真实文本整行完全一致时记为正确
- 字符准确率：基于真实文本与预测文本的编辑距离统计字符级识别准确程度
- 总编辑距离：所有样本预测结果与真实标签之间的编辑距离总和
- 平均编辑距离：总编辑距离除以样本数

指标计算脚本见 [03_eval_baseline.py](/E:/自己的胡思乱想/cnocr_thesis_baseline/scripts/03_eval_baseline.py)。

### 5. Baseline Result Analysis

本文首先基于 CnOCR 预训练模型完成中文单行文本识别 baseline 实验。实验在已配置完成的 `cnocr` 虚拟环境中进行，采用项目预处理后生成的 `sample` 数据集，共 50 张中文文本行图像。实验结果表明，baseline 在 sample 数据集上取得了 0.800 的行准确率和 0.950954 的字符准确率，平均编辑距离为 0.36，说明 CnOCR 预训练模型在当前任务上具备较好的初始识别能力。

从可视化结果来看，识别正确的样本主要集中在文字清晰、排版规则、背景干扰较少的文本图像；识别错误的样本则更多出现在字体模糊、背景复杂、局部遮挡、倾斜弯曲或文本排列特殊的情况下。这说明 baseline 模型对常规中文文本行具有较强识别效果，但在复杂场景下的鲁棒性仍有进一步提升空间。

### 6. Baseline Table Draft

- 样本数：50
- 完全匹配样本数：40
- 行准确率：80.0%
- 字符准确率：95.10%
- 总编辑距离：18
- 平均编辑距离：0.36

### 7. Error Analysis Draft

结合 [baseline_preds.csv](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/preds/baseline_preds.csv) 和 [outputs/figures](/E:/自己的胡思乱想/cnocr_thesis_baseline/outputs/figures) 中的案例可以初步总结：

- 对清晰、规范、背景简单的文本行，模型通常能够给出较准确的识别结果。
- 对模糊、遮挡、复杂背景样本，模型容易出现错字、漏字或局部字符混淆。
- 对竖排文本、倾斜文本及弯曲文本等结构性困难样本，baseline 的稳定性下降更明显。

这些结论可作为后续“困难样本分析”和“模型改进方向”部分的论述基础。

### 8. Next Step Plan

- 在更大的 `test` 集上运行 baseline，获得更有代表性的整体指标。
- 按场景、文档、网页和困难样本类型分别统计结果，形成分组对比。
- 基于错误案例分析决定是否引入数据增强、模型微调或特定类型样本补充。
- 将实验结果整理为论文第五章中的结果表和案例分析图。

## Dual-Modal Module Draft

### 1. 改进思路

针对 baseline 在困难样本、竖排文本和倾斜弯曲文本上的表现不足，本文在原有视觉识别链路基础上增加文本语义辅助分支，构建双模态识别模型。该模型以图像视觉特征为主模态，以字符语义特征为辅助模态，在识别头前通过门控融合实现特征整合，以提升复杂样本条件下的识别鲁棒性。

### 2. 模型结构

- 视觉分支：卷积特征提取 + 序列编码
- 语义分支：字符嵌入 + 双向 GRU
- 融合位置：识别头之前
- 融合方式：门控融合
- 输出：保持与 baseline 一致的字符序列预测结果

### 3. 训练与推理机制

- 训练阶段：语义模态使用真实标签构建
- 推理阶段：语义模态使用视觉分支的初步预测构建

这种设计既保证了训练阶段语义信息稳定，又能在推理阶段保持模型独立完成识别任务，不依赖人工标签输入。

## Hard Cases Experiment Draft

### 1. Hard Cases Evaluation Goal

为了进一步分析 baseline 模型在复杂样本上的识别能力，本研究从测试集中抽取并整理了 905 条困难样本，构建 hard cases 子集。该子集包含背景干扰、模糊、倾斜或弯曲、遮挡以及竖排文本五类典型困难场景，用于分析模型在复杂条件下的鲁棒性。

### 2. Hard Cases Result Summary

在 hard cases 数据集上，CnOCR baseline 取得了 0.179006 的行准确率和 0.324043 的字符准确率，平均编辑距离为 2.867403。与 sample 子集上的初步实验结果相比，baseline 在复杂场景上的性能显著下降，说明模型对困难样本的适应能力明显不足。

### 3. Grouped Hard Cases Analysis

不同困难类型下的实验结果差异明显，具体表现如下：

- `bg_confusion`：104 条，行准确率 11.54%，字符准确率 41.71%
- `blur`：500 条，行准确率 27.00%，字符准确率 41.50%
- `oblique_or_curved`：100 条，行准确率 3.00%，字符准确率 7.83%
- `occlusion`：101 条，行准确率 11.88%，字符准确率 43.17%
- `vertical_text`：100 条，行准确率 0.00%，字符准确率 0.22%

从结果可以看出，当前 baseline 对竖排文本和倾斜弯曲文本最不适应，其中竖排文本几乎无法被正确识别；而模糊样本虽然存在明显性能下降，但相较于竖排和倾斜弯曲文本仍表现出一定的可识别性。

### 4. Hard Cases Discussion Draft

困难样本实验表明，CnOCR 预训练模型在常规中文单行文本上具备一定识别能力，但在版式变化较大、字符方向异常、文字形态扭曲以及视觉干扰增强的条件下，识别效果明显减弱。该现象说明当前 baseline 更适合规则排布的水平文本，对复杂结构文本的泛化能力不足。

这些结果为后续模型改进提供了明确方向：

- 引入更具针对性的困难样本进行训练或微调
- 针对竖排文本和弯曲文本设计专门的数据增强策略
- 在实验章节中将困难样本作为误差分析重点，突出 baseline 的局限性与后续优化空间

### 5. Hard Cases Table Draft

- 样本数：905
- 完全匹配样本数：162
- 行准确率：17.90%
- 字符准确率：32.40%
- 总编辑距离：2595
- 平均编辑距离：2.8674

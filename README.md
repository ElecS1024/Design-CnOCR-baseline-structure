# CnOCR Thesis Baseline

这是一个面向本科毕业设计的 CnOCR baseline 最小项目骨架，目标是先跑通中文单行文本识别 baseline，再为后续微调、实验记录和论文写作留好接口。

## Project Structure

```text
cnocr_thesis_baseline/
├─ data/
├─ scripts/
├─ outputs/
├─ demo/
├─ notebooks/
├─ docs/
├─ requirements.txt
├─ README.md
└─ .gitignore
```

## Quick Start

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 准备样本数据：

- 将 20-50 张单行中文图片放到 `data/sample/`
- 在 `data/labels_sample.csv` 中维护 `filename,text` 两列

3. 依次运行：

```bash
python scripts/01_check_env.py
python scripts/02_run_baseline.py
python scripts/03_eval_baseline.py
python scripts/05_visualize_cases.py
```

4. 后续正式数据集整理：

```bash
python scripts/04_prepare_dataset.py --input-dir data/raw --label-file data/labels_sample.csv
```

## MindOCR Chinese Dataset

如果你使用 MindOCR 中文识别整理集，请先查看：

- `docs/mindocr_dataset.md`

拿到官方 LMDB 数据后，可以直接执行：

```bash
conda run -n cnocr python scripts/06_import_mindocr_lmdb.py
```

## Output Files

- `outputs/preds/baseline_preds.csv`: baseline 预测结果
- `outputs/eval/baseline_metrics.json`: baseline 指标
- `outputs/figures/correct_cases/`: 正确案例
- `outputs/figures/error_cases/`: 错误案例

## Notes

- `01_check_env.py` 和 `02_run_baseline.py` 默认使用当前 `cnocr` 版本自带的默认识别模型
- 如果你想测试特定模型，可以通过 `--rec-model-name` 覆盖
- 建议把每次实验结果同步记录到 `docs/experiment_record.md`

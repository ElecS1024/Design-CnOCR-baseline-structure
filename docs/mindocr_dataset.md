# MindOCR 中文识别整理集接入说明

## 来源

- MindOCR 中文文字识别数据集说明：
  https://mindspore-lab.github.io/mindocr/zh/datasets/chinese_text_recognition/
- FudanVI Benchmarking-Chinese-Text-Recognition：
  https://github.com/FudanVI/benchmarking-chinese-text-recognition

MindOCR 的这套“中文识别整理集”采用的是 FudanVI 整理后的 LMDB 数据格式。

## 下载情况

官方入口不是单个稳定直链，而是：

- Google Drive 文件夹
- 百度网盘

因此在命令行里不一定能一条 `wget/curl` 直接拉完，通常需要你先在浏览器中下载，或使用支持网盘/Drive 的专门工具。

## 建议目录

将下载并解压后的数据放到：

```text
data/raw/mindocr_chinese_text_recognition/
├── training/
├── validation/
└── evaluation/
```

各子目录下应该是 LMDB 文件夹，例如：

```text
training/scene_train/data.mdb
training/scene_train/lock.mdb
validation/scene_val/data.mdb
evaluation/scene_test/data.mdb
```

## 转成当前项目可用格式

运行：

```bash
conda run -n cnocr pip install lmdb
conda run -n cnocr python scripts/06_import_mindocr_lmdb.py
```

脚本会自动：

- 导出 `data/train/`, `data/val/`, `data/test/` 图片
- 生成 `data/labels_train.csv`, `data/labels_val.csv`, `data/labels_test.csv`
- 从训练集前 50 条生成 `data/sample/` 和 `data/labels_sample.csv`

## 快速小规模导入

如果你想先试跑：

```bash
conda run -n cnocr python scripts/06_import_mindocr_lmdb.py --max-samples-per-lmdb 200
```

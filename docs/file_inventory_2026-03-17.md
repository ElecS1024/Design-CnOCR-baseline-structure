# 文件清单（2026-03-17）

| 文件名 | 作用 | 路径 |
|--------|------|------|
| 2026-03-17_work_summary.md | 总结今天完成的工作、当前结果和后续建议 | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\2026-03-17_work_summary.md` |
| experiment_record.md | 记录实验时间、模型、数据集、指标结果和后续实验方向 | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\experiment_record.md` |
| thesis_notes.md | 保存论文写作草稿，包括 baseline 结果、困难样本分析和后续计划 | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\thesis_notes.md` |
| mindocr_dataset.md | 说明 MindOCR 中文识别整理集的来源、目录结构和导入方法 | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\mindocr_dataset.md` |
| file_inventory_2026-03-17.md | 汇总今天生成和整理的文件名、作用与路径，方便后续查阅 | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\file_inventory_2026-03-17.md` |
| README.md | 说明整个 data 目录的用途、数据划分和标签文件含义 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\README.md` |
| README.md | 说明 raw 原始数据目录的用途和当前内容 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\raw\README.md` |
| README.md | 说明 MindOCR 原始 LMDB 数据目录的结构和作用 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\raw\mindocr_chinese_text_recognition\README.md` |
| README.md | 说明 processed 中间数据目录的用途 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\processed\README.md` |
| README.md | 说明 hard_cases_eval 困难样本子集的来源、组成和用途 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\processed\hard_cases_eval\README.md` |
| README.md | 说明 sample 小样本目录的用途和适用脚本 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\sample\README.md` |
| README.md | 说明正式训练集目录的来源、标签和类别组成 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\train\README.md` |
| README.md | 说明正式验证集目录的来源、标签和类别组成 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\val\README.md` |
| README.md | 说明正式测试集目录的来源、类别组成和分组评测依据 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\test\README.md` |
| labels_sample.csv | 保存 sample 小样本图片对应的真实文本标签 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_sample.csv` |
| labels_train.csv | 保存正式训练集图片对应的真实文本标签 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_train.csv` |
| labels_val.csv | 保存正式验证集图片对应的真实文本标签 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_val.csv` |
| labels_test.csv | 保存正式测试集图片对应的真实文本标签 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_test.csv` |
| labels_hard_cases.csv | 保存从测试集中抽出的困难样本子集标签 | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_hard_cases.csv` |
| baseline_preds.csv | 保存 sample baseline 推理结果 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\baseline_preds.csv` |
| hard_cases_preds.csv | 保存 hard cases 子集的 baseline 推理结果 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\hard_cases_preds.csv` |
| test_preds.csv | 保存完整 test 集的 baseline 推理结果 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\test_preds.csv` |
| baseline_metrics.json | 保存 sample baseline 的总体评测指标 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\baseline_metrics.json` |
| hard_cases_metrics.json | 保存 hard cases 子集的总体评测指标 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_metrics.json` |
| test_metrics.json | 保存完整 test 集的总体评测指标 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_metrics.json` |
| group_metrics.csv | 保存 sample baseline 的分组评测结果表 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.csv` |
| group_metrics.json | 保存 sample baseline 的分组评测结果数据 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.json` |
| group_metrics.md | 保存 sample baseline 的分组评测 Markdown 表格 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.md` |
| hard_cases_group_metrics.csv | 保存 hard cases 各困难类型的分组结果表 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.csv` |
| hard_cases_group_metrics.json | 保存 hard cases 各困难类型的分组结果数据 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.json` |
| hard_cases_group_metrics.md | 保存 hard cases 各困难类型的 Markdown 对比表 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.md` |
| test_group_metrics.csv | 保存完整 test 集按 scene、document、web、hard cases 等分组的结果表 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.csv` |
| test_group_metrics.json | 保存完整 test 集按组统计的结果数据 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.json` |
| test_group_metrics.md | 保存完整 test 集按组统计的 Markdown 表格 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.md` |
| summary_table.csv | 保存 sample、hard cases、full test 的总对比结果表 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\summary_table.csv` |
| summary_table.md | 保存 sample、hard cases、full test 的总对比 Markdown 表格 | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\summary_table.md` |
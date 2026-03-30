# 文件清单增强版（2026-03-17）


| 分类   | 文件名                                   | 作用                                                 | 是否可直接用于论文         | 路径                                                                                     |
| ---- | ------------------------------------- | -------------------------------------------------- | ----------------- | -------------------------------------------------------------------------------------- |
| 文档   | 2026-03-17_work_summary.md            | 总结今天完成的工作、当前结果和后续建议                                | 可作为写作参考           | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\2026-03-17_work_summary.md`                     |
| 文档   | experiment_record.md                  | 记录实验时间、模型、数据集、指标结果和后续实验方向                          | 可部分直接引用           | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\experiment_record.md`                           |
| 文档   | thesis_notes.md                       | 保存论文写作草稿，包括 baseline 结果、困难样本分析和后续计划                | 可以直接改写后使用         | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\thesis_notes.md`                                |
| 文档   | mindocr_dataset.md                    | 说明 MindOCR 中文识别整理集的来源、目录结构和导入方法                    | 可作为方法说明参考         | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\mindocr_dataset.md`                             |
| 文档   | file_inventory_2026-03-17.md          | 汇总今天生成和整理的文件名、作用与路径，方便后续查阅                         | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\file_inventory_2026-03-17.md`                   |
| 文档   | file_inventory_2026-03-17_enhanced.md | 按分类整理项目文件，并增加论文可用性标记                               | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\docs\file_inventory_2026-03-17_enhanced.md`          |
| 数据说明 | README.md                             | 说明整个 data 目录的用途、数据划分和标签文件含义                        | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\README.md`                                      |
| 数据说明 | README.md                             | 说明 raw 原始数据目录的用途和当前内容                              | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\raw\README.md`                                  |
| 数据说明 | README.md                             | 说明 MindOCR 原始 LMDB 数据目录的结构和作用                      | 可作为数据来源说明参考       | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\raw\mindocr_chinese_text_recognition\README.md` |
| 数据说明 | README.md                             | 说明 processed 中间数据目录的用途                             | 不直接用于论文           | `E:\自己的胡混乱想\cnocr_thesis_baseline\data\processed\README.md`                            |
| 数据说明 | README.md                             | 说明 hard_cases_eval 困难样本子集的来源、组成和用途                 | 可作为困难样本说明参考       | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\processed\hard_cases_eval\README.md`            |
| 数据说明 | README.md                             | 说明 sample 小样本目录的用途和适用脚本                            | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\sample\README.md`                               |
| 数据说明 | README.md                             | 说明正式训练集目录的来源、标签和类别组成                               | 可作为数据集构建说明参考      | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\train\README.md`                                |
| 数据说明 | README.md                             | 说明正式验证集目录的来源、标签和类别组成                               | 可作为实验设置说明参考       | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\val\README.md`                                  |
| 数据说明 | README.md                             | 说明正式测试集目录的来源、类别组成和分组评测依据                           | 可作为测试集说明参考        | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\test\README.md`                                 |
| 数据   | labels_sample.csv                     | 保存 sample 小样本图片对应的真实文本标签                           | 可作为附录或示例          | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_sample.csv`                              |
| 数据   | labels_train.csv                      | 保存正式训练集图片对应的真实文本标签                                 | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_train.csv`                               |
| 数据   | labels_val.csv                        | 保存正式验证集图片对应的真实文本标签                                 | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_val.csv`                                 |
| 数据   | labels_test.csv                       | 保存正式测试集图片对应的真实文本标签                                 | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_test.csv`                                |
| 数据   | labels_hard_cases.csv                 | 保存从测试集中抽出的困难样本子集标签                                 | 可作为困难样本来源依据       | `E:\自己的胡思乱想\cnocr_thesis_baseline\data\labels_hard_cases.csv`                          |
| 结果   | baseline_preds.csv                    | 保存 sample baseline 推理结果                            | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\baseline_preds.csv`                    |
| 结果   | hard_cases_preds.csv                  | 保存 hard cases 子集的 baseline 推理结果                    | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\hard_cases_preds.csv`                  |
| 结果   | test_preds.csv                        | 保存完整 test 集的 baseline 推理结果                         | 不直接用于论文           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\preds\test_preds.csv`                        |
| 结果   | baseline_metrics.json                 | 保存 sample baseline 的总体评测指标                         | 可整理成论文表格          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\baseline_metrics.json`                  |
| 结��� | hard_cases_metrics.json               | 保存 hard cases 子集的总体评测指标                            | 可整理成论文表格          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_metrics.json`                |
| 结果   | test_metrics.json                     | 保存完整 test 集的总体评测指标                                 | 可直接用于论文结果表        | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_metrics.json`                      |
| 结果   | group_metrics.csv                     | 保存 sample baseline 的分组评测结果表                        | 可作为内部参考           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.csv`                      |
| 结果   | group_metrics.json                    | 保存 sample baseline 的分组评测结果数据                       | 可作为内部参考           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.json`                     |
| 结果   | group_metrics.md                      | 保存 sample baseline 的分组评测 Markdown 表格               | 可作为内部参考           | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\group_metrics.md`                       |
| 结果   | hard_cases_group_metrics.csv          | 保存 hard cases 各困难类型的分组结果表                          | 可整理成论文分组对比表       | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.csv`           |
| 结果   | hard_cases_group_metrics.json         | 保存 hard cases 各困难类型的分组结果数据                         | 可作为内部分析依据         | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.json`          |
| 结果   | hard_cases_group_metrics.md           | 保存 hard cases 各困难类型的 Markdown 对比表                  | 可直接改写进论文          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\hard_cases_group_metrics.md`            |
| 结果   | test_group_metrics.csv                | 保存完整 test 集按 scene、document、web、hard cases 等分组的结果表 | 可整理成论文核心对比表       | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.csv`                 |
| 结果   | test_group_metrics.json               | 保存完整 test 集按组统计的结果数据                               | 可作为内部分析依据         | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.json`                |
| 结果   | test_group_metrics.md                 | 保存完整 test 集按组统计的 Markdown 表格                       | 可直接改写进论文          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\test_group_metrics.md`                  |
| 结果   | summary_table.csv                     | 保存 sample、hard cases、full test 的总对比结果表             | 可整理成论文总表          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\summary_table.csv`                      |
| 结果   | summary_table.md                      | 保存 sample、hard cases、full test 的总对比 Markdown 表格    | 可直接改写进论文          | `E:\自己的胡思乱想\cnocr_thesis_baseline\outputs\eval\summary_table.md`                       |
| 脚本   | 01_check_env.py                       | 检查 Python、Torch、CnOCR、OpenCV 和模型加载是否正常             | 不用于论文正文，可用于复现实验环境 | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\01_check_env.py`                             |
| 脚本   | 02_run_baseline.py                    | 运行 baseline OCR 推理并生成预测结果                          | 可在方法实现部分描述        | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\02_run_baseline.py`                          |
| 脚本   | 03_eval_baseline.py                   | 计算总体评测指标                                           | 可在评价指标与实验流程部分描述   | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\03_eval_baseline.py`                         |
| 脚本   | 04_prepare_dataset.py                 | 用于原始数据清洗、划分和生成标签                                   | 可在数据集构建部分描述       | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\04_prepare_dataset.py`                       |
| 脚本   | 05_visualize_cases.py                 | 生成正确与错误案例可视化结果                                     | 可在误差分析部分描述        | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\05_visualize_cases.py`                       |
| 脚本   | 06_import_mindocr_lmdb.py             | 将 MindOCR/Fudan 的 LMDB 数据导入成图片和 CSV                | 可在数据预处理部分描述       | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\06_import_mindocr_lmdb.py`                   |
| 脚本   | 07_group_eval.py                      | 按数据来源和困难类型对预测结果进行分组评测                              | 可在分组实验部分描述        | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\07_group_eval.py`                            |
| 脚本   | 08_build_summary_table.py             | 汇总 sample、hard cases、full test 等总体指标形成总对比表         | 可在结果整理方法中简述       | `E:\自己的胡思乱想\cnocr_thesis_baseline\scripts\08_build_summary_table.py`                   |



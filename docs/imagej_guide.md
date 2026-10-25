# 用 ImageJ/Fiji 标注 FDI 框

## 准备

1. 打开 Fiji/ImageJ；
2. `Analyze > Tools > ROI Manager` 打开 ROI Manager；
3. `File > Open` 打开 `FDI_annotation.ijm`；
4. `Macros > Install`（或把 .ijm 拖进 ImageJ 窗口）。

装好后，菜单 `Macros` 里会有：

- `FDI: Add ROI [a]`
- `FDI: Save CSV [s]`

## 每张图怎么标

1. 打开一张全景片；
2. 选矩形工具；
3. 框住一颗牙；
4. 按 **a**，输入 FDI（如 16、46、55）；
5. 重复 3–4，把所有可见牙框完；
6. 按 **s**，自动：
   - 存 `<图名>_ROI.zip`
   - Measure 全部 ROI，存 `<图名>_measure.csv`
   - 清空 ROI Manager
   - 关闭当前图，打开下一张

所以标完一张只要按一次 **s**，不用手动 Measure/Delete/开下一张。

## 规则

- 一颗牙一个框，不合并邻牙；
- 缺失牙不画；
- 阻生/未萌但结构可见要画；
- 乳牙写 51–85，恒牙写 11–48；
- 先确认左右：图像左侧 = 患者右侧。

## 没装宏的备用做法

1. 矩形工具画框；
2. `Ctrl+T` 加入 ROI Manager；
3. 双击 ROI 名称，改成 FDI；
4. 全部画完 `More > Save` 存 ROI；
5. `Measure` 导出 X/Y/Width/Height，再转 x1,y1,x2,y2。

## 交回

把每张图的 `*_fdi.csv` 一起给我；我用 `scripts/imagej_csv_merge.py` 合并成训练用 CSV。

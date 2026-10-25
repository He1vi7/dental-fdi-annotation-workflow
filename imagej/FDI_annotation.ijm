// ImageJ/Fiji: 画矩形 -> 按 a 输入 FDI -> 按 s 保存 CSV/ROI
// 先打开 ROI Manager（Analyze > Tools > ROI Manager）

macro "FDI: Add ROI [a]" {
    if (selectionType() != 0) {
        exit("请先用矩形工具画一个框");
    }
    roiManager("Add");
    fdi = getString("FDI 编号（如 16 / 55）:", "");
    if (fdi == "") {
        roiManager("Delete");
        exit();
    }
    roiManager("Rename", fdi);
}

macro "FDI: Rename [r]" {
    if (roiManager("count") <= 0) exit("先用 Ctrl+T 加入 ROI");
    fdi = getString("FDI 编号（如 16 / 55）:", "");
    if (fdi == "") exit;
    roiManager("Rename", fdi);
}

macro "FDI: Save CSV [s]" {
    n = roiManager("count");
    if (n <= 0) exit("ROI Manager 里没有框");
    title = getTitle();
    dir = getDirectory("image");
    base = title;
    if (endsWith(base, ".png")) base = substring(base, 0, lengthOf(base) - 4);
    if (endsWith(base, ".jpg")) base = substring(base, 0, lengthOf(base) - 4);
    csv = dir + base + "_fdi.csv";
    roiManager("Save", dir + base + "_ROI.zip");
    f = File.open(csv);
    print(f, "文件名,FDI,x1,y1,x2,y2,presence,备注");
    for (i = 0; i < n; i++) {
        roiManager("Select", i);
        run("Restore Selection");
        getSelectionBounds(x, y, w, h);
        name = Roi.getName();
        print(f, title + "," + name + "," + x + "," + y + "," + (x + w) + "," + (y + h) + ",,");
    }
    File.close(f);
    showMessage("已保存", csv);
}

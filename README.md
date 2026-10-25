# Dental Panoramic FDI Annotation Workflow

A small, reproducible workflow for dental panoramic image annotation, FDI
numbering, ImageJ/Fiji ROI export, AnyLabeling + MobileSAM setup, YOLO dataset
conversion, and YOLOv8n-FDI baseline training.

> This repository contains code and documentation only. It does not contain
> patient images, medical records, annotation datasets, or trained weights.
> It is a research workflow demo, not a clinical diagnostic system.

## Features

- ImageJ/Fiji macro for drawing a rectangular tooth ROI, entering its FDI code,
  and exporting ROI and CSV records.
- AnyLabeling configuration for 52 FDI classes, annotation flags, automatic
  saving, and a MobileSAM interactive segmentation setup.
- Conversion from ImageJ `Measure` CSV to a unified FDI box table.
- Conversion from FDI boxes to a YOLO detection dataset.
- YOLOv8n-FDI baseline training script with horizontal flipping disabled to
  avoid left/right quadrant label conflicts.
- Early post-processing for missing-tooth candidates using age-dependent
  dental templates and neighborhood checks.

## Repository layout

```text
.
├─ imagej/
│  └─ FDI_annotation.ijm
├─ anylabeling/
│  ├─ anylabeling_config.example.yaml
│  └─ launch.example.bat
├─ scripts/
│  ├─ imagej_batch_convert.py
│  ├─ prepare_yolo_dataset.py
│  ├─ train_yolov8_fdi.py
│  └─ arch_postprocess.py
├─ docs/
│  ├─ annotation_rules.md
│  └─ imagej_guide.md
├─ requirements.txt
└─ .gitignore
```

## Quick start

### 1. ImageJ/Fiji

1. Open the ROI Manager.
2. Install `imagej/FDI_annotation.ijm` through `Macros > Install`.
3. Draw a rectangle around one visible tooth.
4. Press `a`, enter an FDI code, and repeat for all visible teeth.
5. Press `s` to save a `*_fdi.csv` file and a `*_ROI.zip` beside the image.

See [docs/imagej_guide.md](docs/imagej_guide.md) for the full workflow.

### 2. AnyLabeling + MobileSAM

Copy `anylabeling/anylabeling_config.example.yaml`, update local paths if
needed, and start AnyLabeling with your own environment:

```powershell
anylabeling `
  --config .\anylabeling\anylabeling_config.example.yaml `
  --output .\outputs\annotations `
  --autosave `
  --nodata `
  .\data\images
```

Install MobileSAM through the AnyLabeling model manager before using the
interactive segmentation model.

### 3. Convert annotations and prepare YOLO data

```powershell
python scripts/imagej_batch_convert.py `
  --dir data/imagej_csv `
  --images data/images `
  --out data/fdi_boxes.csv

python scripts/prepare_yolo_dataset.py `
  --labels data/fdi_boxes.csv `
  --images data/images `
  --out data/yolo_fdi
```

The unified CSV schema is:

```text
文件名,FDI,x1,y1,x2,y2,presence,备注
```

### 4. Train a baseline

```powershell
python scripts/train_yolov8_fdi.py `
  --data data/yolo_fdi/data.yaml `
  --base yolov8n.pt `
  --epochs 80 `
  --imgsz 1280 `
  --batch 4 `
  --fliplr 0
```

Horizontal flipping is disabled because FDI labels encode left/right
quadrants. A flipped image would keep the original FDI labels while changing
their anatomical meaning.

## Evaluation status

The workflow was developed in an ongoing undergraduate research project and
validated on a private annotation batch. The private batch produced 50 annotated
panoramic images and 1,525 FDI ROI records. Those source images and annotation
records are intentionally excluded from this repository.

The included YOLO configuration is an early baseline for validating the
annotation-to-training pipeline. No clinical performance claim is made.

## Privacy and responsible use

- Do not commit patient images, DICOM files, reports, names, dates of birth, or
  other personal or medical information.
- Remove burned-in names or identifiers before using any image for a public demo.
- Use synthetic or fully de-identified images in screenshots and examples.
- Review the repository for local absolute paths before publishing.
- This code is not medical software and must not be used for diagnosis or
  treatment decisions.

## Limitations

- The missing-tooth post-processing script uses an early age-based template and
  requires manual review.
- The model baseline is trained on a small pilot set.
- Annotation quality depends on consistent FDI rules and overlapping-tooth
  handling.
- Validation on an independent patient-level test set is still required.


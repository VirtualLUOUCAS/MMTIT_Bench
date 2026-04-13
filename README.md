# MMTIT-Bench

**A Multilingual and Multi-Scenario Benchmark with Cognition–Perception–Reasoning Guided Text-Image Machine Translation**

<p align="center">
  <a href="https://huggingface.co/datasets/VirtualLUO/MMTIT_Bench/blob/main/README_ZH.md">中文版</a> •
  <a href="https://arxiv.org/abs/2603.23896">Paper</a> •
  <a href="https://github.com/VirtualLUOUCAS/MMTIT_Bench">GitHub</a> •
  <a href="https://huggingface.co/datasets/VirtualLUO/MMTIT_Bench">HuggingFace</a>
</p>

## Overview

**MMTIT-Bench** is a human-verified benchmark for end-to-end Text-Image Machine Translation (TIMT). It contains **1,400 images** spanning **14 non-English and non-Chinese languages** across diverse real-world scenarios, with bilingual (Chinese & English) translation annotations.

We also propose **CPR-Trans** (Cognition–Perception–Reasoning for Translation), a reasoning-oriented data paradigm that unifies scene cognition, text perception, and translation reasoning within a structured chain-of-thought framework.

<p align="center">
  <img src="assets/overview.png" width="90%" alt="MMTIT-Bench Overview">
</p>

## Benchmark Statistics

| Item | Details |
|------|---------|
| Total Images | 1,400 |
| Languages | 14 (AR, DE, ES, FR, ID, IT, JA, KO, MS, PT, RU, TH, TR, VI) |
| Translation Directions | Other→Chinese, Other→English |
| Scenarios | Documents, Menus, Books, Attractions, Posters, Commodities, etc. |
| Annotation | Human-verified OCR + Bilingual translations |

## Data Format

### Directory Structure

```
MMTIT-Bench/
├── README.md
├── README_ZH.md
├── annotation.jsonl        # Benchmark annotations
├── images.zip              # Benchmark images
├── eval_comet_demo.py      # COMET evaluation script
└── prediction_demo.jsonl   # Example prediction file
```

### Annotation (`annotation.jsonl`)

Each line is a JSON object:

```json
{
    "image_id": "Korea_Menu_20843.jpg",
    "parsing_anno": "멜로우스트리트\n\n위치: 서울특별시 관악구...",
    "translation_zh": "梅尔街\n\n位置：首尔特别市 冠岳区...",
    "translation_en": "Mellow Street\n\nLocation: 1st Floor, 104 Gwanak-ro..."
}
```

| Field | Description |
|-------|-------------|
| `image_id` | Image filename, formatted as `{Language}_{Scenario}_{ID}.jpg` |
| `parsing_anno` | OCR text parsing annotation (source language) |
| `translation_zh` | Chinese translation |
| `translation_en` | English translation |

### Prediction File

Your prediction file should be a JSONL with the following fields:

```json
{"image_id": "Korea_Menu_20843.jpg", "pred": "Your model's translation output"}
```

## Evaluation

We use [COMET](https://github.com/Unbabel/COMET) (`Unbabel/wmt22-comet-da`) as the rule-based evaluation metric.

### Install

```bash
pip install unbabel-comet
```

### Run

```bash
# Other → Chinese
python eval_comet_demo.py \
    --prediction your_prediction.jsonl \
    --annotation annotation.jsonl \
    --direction other2zh \
    --batch_size 16 --gpus 0

# Other → English
python eval_comet_demo.py \
    --prediction your_prediction.jsonl \
    --annotation annotation.jsonl \
    --direction other2en \
    --batch_size 16 --gpus 1
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--prediction` | *(required)* | Path to your prediction JSONL |
| `--annotation` | `annotation.jsonl` | Path to benchmark annotations |
| `--direction` | *(required)* | `other2zh` or `other2en` |
| `--batch_size` | `16` | Batch size for inference |
| `--gpus` | `0` | Number of GPUs (0 = CPU) |
| `--output` | `comet_results_{direction}.jsonl` | Output path for per-sample scores |

## Citation

```bibtex
@misc{li2026mmtitbench,
      title={MMTIT-Bench: A Multilingual and Multi-Scenario Benchmark with Cognition-Perception-Reasoning Guided Text-Image Machine Translation},
      author={Gengluo Li and Chengquan Zhang and Yupu Liang and Huawen Shen and Yaping Zhang and Pengyuan Lyu and Weinong Wang and Xingyu Wan and Gangyan Zeng and Han Hu and Can Ma and Yu Zhou},
      year={2026},
      journal={arXiv preprint arXiv:2603.23896},
      url={https://arxiv.org/abs/2603.23896},
}
```

## License

This benchmark is released for **research purposes only**.

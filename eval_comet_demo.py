"""
MMTIT-Bench COMET Evaluation Demo

Prediction file format (JSONL):
    {"image_id": "Korea_Menu_20843.jpg", "pred": "梅尔街 ..."}

Usage:
    python eval_comet_demo.py \
        --prediction prediction.jsonl \
        --annotation annotation.jsonl \
        --direction other2zh \
        --batch_size 16 --gpus 0
"""

import json
import argparse
from comet import download_model, load_from_checkpoint


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="MMTIT-Bench COMET Evaluation")
    parser.add_argument("--prediction", type=str, required=True, help="Path to prediction JSONL (fields: image_id, pred)")
    parser.add_argument("--annotation", type=str, default="annotation.jsonl", help="Path to annotation JSONL")
    parser.add_argument("--direction", type=str, required=True, choices=["other2zh", "other2en"], help="Translation direction")
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--gpus", type=int, default=0, help="0 for CPU")
    parser.add_argument("--output", type=str, default=None, help="Output path for per-sample scores")
    args = parser.parse_args()

    if args.output is None:
        args.output = f"comet_results_{args.direction}.jsonl"

    # Choose reference field based on direction
    ref_key = "translation_zh" if args.direction == "other2zh" else "translation_en"

    # Load data
    annotations = {item["image_id"]: item for item in load_jsonl(args.annotation)}
    predictions = load_jsonl(args.prediction)
    print(f"Annotations: {len(annotations)}, Predictions: {len(predictions)}")

    # Merge by image_id -> build COMET inputs (src / mt / ref)
    comet_inputs = []
    matched_ids = []
    for pred in predictions:
        img_id = pred["image_id"]
        if img_id in annotations:
            ann = annotations[img_id]
            comet_inputs.append({
                "src": ann["parsing_anno"],  # source OCR text
                "mt":  pred["pred"],          # model prediction
                "ref": ann[ref_key],          # ground-truth translation
            })
            matched_ids.append(img_id)

    print(f"Matched: {len(comet_inputs)} / {len(predictions)}")
    assert len(comet_inputs) > 0, "No matching samples found. Check image_id consistency."

    # Load COMET model and evaluate
    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)
    model_output = model.predict(comet_inputs, batch_size=args.batch_size, gpus=args.gpus)

    # Print system score
    print(f"\n{'='*50}")
    print(f"  Direction:    {args.direction}")
    print(f"  Samples:      {len(comet_inputs)}")
    print(f"  COMET Score:  {model_output.system_score:.4f}")
    print(f"{'='*50}")

    # Save per-sample results
    with open(args.output, "w", encoding="utf-8") as f:
        for img_id, score in zip(matched_ids, model_output.scores):
            f.write(json.dumps({"image_id": img_id, "comet_score": score}, ensure_ascii=False) + "\n")
    print(f"Per-sample scores saved to: {args.output}")


if __name__ == "__main__":
    main()

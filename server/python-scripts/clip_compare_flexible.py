# clip_compare_flexible_json_detailed_decision.py

import sys
import json
import torch
import clip
from PIL import Image

def load_image(image_path):
    return Image.open(image_path).convert("RGB")

def main():
    output = {
        "image_similarity": None,
        "text_similarity": None,
        "decision": "",
        "details": "",
        "is_image_similar": False,
        "is_text_similar": False,
        "thresholds": {
            "image": 0.3,
            "text": 0.3,
            "image_strict": 0.8
        }
    }

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        output["decision"] = "Error: Incorrect number of arguments"
        print(json.dumps(output))
        sys.exit(1)

    ref_image_path = sys.argv[1]
    compare_image_path = sys.argv[2]
    text_label = sys.argv[3] if len(sys.argv) == 4 else None

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    ref_img = preprocess(load_image(ref_image_path)).unsqueeze(0).to(device)
    cmp_img = preprocess(load_image(compare_image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        # Encode and normalize images
        ref_features = model.encode_image(ref_img)
        cmp_features = model.encode_image(cmp_img)
        ref_features_norm = ref_features / ref_features.norm(dim=-1, keepdim=True)
        cmp_features_norm = cmp_features / cmp_features.norm(dim=-1, keepdim=True)

        # Image similarity
        img_similarity = (ref_features_norm @ cmp_features_norm.T).item()
        output["image_similarity"] = img_similarity
        output["is_image_similar"] = img_similarity > output["thresholds"]["image"]

        decision = "Images are not similar."

        if text_label:
            # Text similarity
            text_tokens = clip.tokenize([text_label]).to(device)
            text_features = model.encode_text(text_tokens)
            text_features_norm = text_features / text_features.norm(dim=-1, keepdim=True)
            text_similarity = (cmp_features_norm @ text_features_norm.T).item()
            output["text_similarity"] = text_similarity
            output["is_text_similar"] = text_similarity > output["thresholds"]["text"]

            # Detailed decision logic
            if output["is_image_similar"] and output["is_text_similar"]:
                decision = "Images and text match"
            elif output["is_image_similar"]:
                decision = "Images match but text does not"
            elif output["is_text_similar"]:
                decision = "Text matches but images do not"
            else:
                decision = "Neither images nor text match"
        else:
            # Decision without tag
            if img_similarity > output["thresholds"]["image_strict"]:
                decision = "Images are highly similar!"
            elif img_similarity > output["thresholds"]["image"]:
                decision = "Images are moderately similar"
            else:
                decision = "Images are not similar"

        output["decision"] = decision
        output["details"] = f"Image similarity: {img_similarity:.4f}" + \
                            (f", Text similarity ('{text_label}'): {text_similarity:.4f}" if text_label else "") + \
                            f", Image threshold: {output['thresholds']['image']}, Strict threshold: {output['thresholds']['image_strict']}" + \
                            (f", Text threshold: {output['thresholds']['text']}" if text_label else "")

    print(json.dumps(output))

if __name__ == "__main__":
    main()

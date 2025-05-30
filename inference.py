import os
import argparse
import json
from tqdm import tqdm
import shutil

input_file = 'closed_standard_en.jsonl'
output_file = 'closed_standard_en_output.jsonl'

def main():
    # Step 1: Build your model (placeholder)
    # model = model.cuda()
    # model.eval()

    # Step 2: Inference
    with open(input_file, "r") as fin, open(output_file, "w") as fout:
        for line in tqdm(fin):
            item = json.loads(line.strip())
            audio_path = item['audio_path']
            if not os.path.exists(audio_path):
                print(f"Missing audio file: {audio_path}")
                continue

            instruction = "You are a helpful AI assistant. Please answer the question based on the provided audio."

            # Step 3: Run model inference
            # output = model.infer(Prompts=instruction, Audio_path=audio_path, ...)
            output = "dummy response"  # ← Replace with actual model output

            item['response'] = output
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()

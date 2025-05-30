from tqdm import tqdm
import multiprocessing
import json
from openai import OpenAI
from api import generate_text_chat
from argparse import ArgumentParser
from judge_prompts import get_api_prompt

client = OpenAI(api_key="YourAPIKey")


def generate(item, data_type, prompt):
    if "decomposed_questions" in item:
        prompt = prompt.replace('{prompt}', item['prompt']).replace('{decompose_question}', item['decomposed_questions']).replace('{response}', item['response'])
    else:
        prompt = prompt.replace("{prompt}", item['prompt']).replace('{response}', item['response'])
    rtn = [
        item.message.content.strip() for item in generate_text_chat(
            client=client,
            model='gpt-4o-mini',
            messages=[{"role": "system",
                       "content": "You are a helpful assistant who tries to help answer the user's question."},
                      {"role": "user", "content": prompt}],
            max_tokens=1024,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            temperature=0.5, top_p=0.95, n=4  # Generate multiple completions to assess response stability and reliability
        ).choices
    ]
    item[f"pred_score"] = rtn
    return item



def main():
    parser = ArgumentParser()
    parser.add_argument('--data_type', type=str, default='open')
    parser.add_argument('--input_file', type=str, default='')
    args = parser.parse_args()

    file_path = args.input_file
    data_type = args.data_type


    meta_prompt = get_api_prompt(data_type)
    data = []

    with open(file_path, 'r') as f:
        for line in f:
            json_obj = json.loads(line.strip())
            data.append(json_obj)

    ### evaluate data
    # with multiprocessing.Pool(10) as pool:
    #     scores = list(tqdm(pool.imap(generate, data, data_type, meta_prompt), total=len(data)))
    
    # Evaluate data
    scores = []
    for item in data:
        score = generate(item, data_type, meta_prompt)
        scores.append(score)


    # Write to a temporary file
    temp_file = file_path + '.tmp'
    try:
        with open(temp_file, 'w') as f:
            for json_obj in scores:
                f.write(json.dumps(json_obj) + '\n')

        # Replace original file with the temporary file
        os.replace(temp_file, file_path)

    except Exception as e:
        print(f"An error occurred while writing to {file_path}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)




if __name__ == '__main__':
    main()

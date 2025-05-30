from argparse import ArgumentParser
import json
from evaluator import evaluator_mapping
from loguru import logger



def main():
    parser = ArgumentParser()
    parser.add_argument('--src_file', type=str, default='')
    parser.add_argument('--evaluator', type=str, default='close', choices=list(evaluator_mapping.keys()))
    args = parser.parse_args()
    data = []
    with open(args.src_file, 'r') as f:
        for line in f:
            json_obj = json.loads(line.strip())  # Convert JSON string to dictionary
            data.append(json_obj)

    evaluator = evaluator_mapping[args.evaluator]()
    logger.info(evaluator.evaluate(data))


if __name__ == "__main__":
    main()

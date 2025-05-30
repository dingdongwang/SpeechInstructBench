# SpeechInstructBench: Speech Instruction Following Benchmark

This repo contains the evaluation code of:
[SpeechInstructBench: Speech Instruction Following Benchmark](https://arxiv.org/abs/2503.02769)


## Table of Contents
- [**Leaderboard**](#leaderboard)
- [**Setup**](#setup)
- [**Dataset**](#dataset)
- [**Evaluation**](#evaluation)
- [**Citation**](#citation)

## Leaderboard

| SpeechLLMs     | Closed-Ended                                                                                   |                        |                        |                              |                            | Open-Ended             | Adjustment            |
|----------------|-----------------------------------------------------------------------------------------------|------------------------|------------------------|------------------------------|----------------------------|------------------------|------------------------|
|                | Standard (P./I. Acc)↑ | Background (P./I. Acc)↑ | Accent (P./I. Acc)↑ | Paralinguistics (P./I. Acc)↑ | Disfluency (P./I. Acc)↑ | Standard (P./I. Acc)↑ | Standard (IAR↑/ ECR↓)       |
| ***English***     |                          |                           |                         |                                |                              |                          |                          |
| BLSP           | 14.97 / 24.17             | 13.76 / 23.46              | 13.28 / 22.89            | 13.65 / 23.60                   | 13.10 / 22.88                | 11.78 / 21.55              | 35.45 / 35.05            |
| GLM-4-Voice    | 18.28 / 29.39             | 17.29 / 27.89              | 20.37 / 31.11            | 20.04 / 31.75                   | 18.83 / 30.18                | 28.17 / 52.05              | 77.91 / 24.89            |
| Mini-Omni2     | 7.04 / 16.52              | 7.26 / 16.52               | 7.80 / 16.91             | 6.16 / 15.59                    | 7.92 / 16.30                 | 3.23 / 6.84                | 12.80 / 21.20            |
| Mini-Omni      | 8.14 / 16.73              | 9.25 / 17.74               | 8.37 / 16.88             | 8.14 / 18.02                    | 8.23 / 17.52                 | 1.15 / 1.70                | 7.31 / 18.69             |
| Megrez         | 19.49 / 31.04             | 17.51 / 28.96              | 18.31 / 29.18            | 19.02 / 30.53                   | 19.28 / 28.67                | 37.27 / 64.35              | 55.06 / 31.98            |
| DIVA           | 27.64 / 37.26             | 26.32 / 36.69              | 26.49 / 36.26            | 27.97 / 37.91                   | 19.16 / 27.89                | 33.64 / 61.12              | 58.94 / 33.73            |
| Qwen2-Audio    | 19.82 / 30.18             | 18.17 / 28.82              | 18.59 / 28.81            | 20.70 / 31.33                   | 15.19 / 24.67                | 31.40 / 58.14              | 48.60 / 37.45            |
| InSerter       | 39.75 / 51.35             | 37.56 / 49.87              | 37.34 / 48.24            | 35.79 / 46.85                   | 36.38 / 47.28                | 40.87 / 67.33              | 80.72 / 23.28            |
| ***Chinese***      |                          |                           |                         |                                |                              |                          |                          |
| GLM-4-Voice    | 18.31 / 26.72             | 16.58 / 23.99              | 12.64 / 20.86            | 17.28 / 25.76                   | 14.51 / 22.87                | 39.03 / 56.52              | 81.27 / 13.15            |
| Megrez         | 18.31 / 27.84             | 17.16 / 26.32              | 17.26 / 26.01            | 18.43 / 27.97                   | 16.58 / 25.76                | 31.69 / 39.27              | 63.34 / 17.53            |
| DIVA           | 15.86 / 26.43             | 17.05 / 25.92              | 11.71 / 21.18            | 15.55 / 24.87                   | 14.97 / 24.31                | 10.62 / 31.10              | 25.94 / 13.39            |
| Qwen2-Audio    | 19.23 / 28.97             | 18.89 / 28.49              | 17.99 / 26.99            | 18.77 / 26.48                   | 18.77 / 26.48                | 40.64 / 64.37              | 64.00 / 23.20            |
| InSerter       | 32.71 / 42.37             | 32.60 / 42.30              | 27.95 / 36.15            | 33.99 / 43.18                   | 32.48 / 41.33                | 50.58 / 68.32              | 84.06 / 12.10            |

We encourage you to submit new SpeechInstructBench results directly through the issue tracker. The ranking list will be updated accordingly.

## Setup
```shell
conda create -n speechinstructbench python=3.10
conda activate speechinstructbench
pip install -r requirements.txt
```

## Dataset

The SpeechInstructBench dataset is available at [HuggingFace](https://huggingface.co/datasets/ddwang2000/SpeechInstructBench)

## Evaluation
### Step 1: Inference your model on SpeechInstructBench
To obtain the responses from your model, refer to the following command:
```shell
python inference.py
```
This command applies to all datasets in SpeechInstructBench, which includes closed-ended, open-ended, and adjustment instruction-following tasks. For the closed-ended instruction-following task, there are several subtasks with different audio variants (e.g., accent, background noise, disfluency versions). Each task has both Chinese and English dataset versions.

### Step 2: Obtain the GPT score for the Open-Ended and Adjustment subtasks of SpeechInstructBench.
For datasets `open-ended` and `adjustment`, we use `gpt-4o-mini` to evaluate the responses. Run the following command to get the GPT score:
```shell
python api_judge.py --data_type open --src_file open_ended_en.jsonl
```
The GPT evaluation scores will be saved to the JSONL file specified by `--src_file` jsonl path, with each entry containing a new key `pred_score`.

You can skip this step for the closed-ended subtask of SpeechInstructBench. For the` --data_type`, options includes `open` and `adjust`, which correspond to the open-ended and adjustment subtasks, respectively. Each task has both Chinese and English dataset versions.

### Step3: Calculate the Final Results
To get the final evaluation results, run:
```shell
python evaluate.py --evaluator open --src_file open_ended_en.jsonl
```
**Arguments:**
- `--evaluator`: Specifies the evaluator type:
    - Use `open` for open-ended task.
    - Use `close` for closed-ended task.
    - Use `adjust` for adjustment task.
- `--src_file`: Specifies the jsonl path need to be evaluated.

## Citation
If you use the SpeechInstructBench or InSerter in your research, please cite the following paper:
```
@article{wang2025inserterspeechinstructionfollowing,
      title={InSerter: Speech Instruction Following with Unsupervised Interleaved Pre-training}, 
      author={Dingdong Wang and Jin Xu and Ruihang Chu and Zhifang Guo and Xiong Wang and Jincenzi Wu and Dongchao Yang and Shengpeng Ji and Junyang Lin},
      journal={arXiv preprint arXiv:2503.02769},
      year={2025}
}
```
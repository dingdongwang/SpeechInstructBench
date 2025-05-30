# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Binary of evaluating instruction following. See README.md."""

import collections
import dataclasses
import json
import os
from .base import Evaluator
import ast
import statistics


def get_majority_scores(entry):
    raw_scores = entry["pred_score"]

    parsed_lists = []
    for s in raw_scores:
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                parsed_lists.append(parsed)
        except:
            continue

    max_len = max(len(lst) for lst in parsed_lists) if parsed_lists else 0
    filtered_lists = [lst for lst in parsed_lists if len(lst) == max_len]

    if not filtered_lists:
        return []

    transposed = list(zip(*filtered_lists))  # list of tuples
    majority_scores = []
    for position_scores in transposed:
        try:
            majority = statistics.mode(position_scores)
            majority_scores.append(majority)
        except statistics.StatisticsError:
            majority_scores.append("NO")  

    return majority_scores



class OpenEvaluator(Evaluator):
    def evaluate(self, data):
        total_prompts = 0
        correct_prompts = 0
        total_instructions = 0
        correct_instructions = 0

        for entry in data:
            majority_scores = get_majority_scores(entry)

            if not majority_scores:
                continue

            total_prompts += 1
            total_instructions += len(majority_scores)
            correct_this_prompt = all(s == "YES" for s in majority_scores)
            correct_this_instruction = sum(1 for s in majority_scores if s == "YES")

            if correct_this_prompt:
                correct_prompts += 1
            correct_instructions += correct_this_instruction

        prompt_acc = correct_prompts / total_prompts if total_prompts > 0 else 0
        instr_acc = correct_instructions / total_instructions if total_instructions > 0 else 0

        print(f"Prompt-level Accuracy: {prompt_acc:.4f}")
        print(f"Instruction-level Accuracy: {instr_acc:.4f}")





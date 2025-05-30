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


class AdjustEvaluator(Evaluator):
    def evaluate(self, data):
        iar_values = []
        ecr_values = []
        for entry in data:
            scores = entry.get("pred_score", [])

            follow_after_adjust_values = []
            follow_before_adjust_values = []
            after_adjust_content_correct_values = []

            for score in scores:
                try:
                    score_dict = json.loads(score)
                    follow_after_adjust_values.append(score_dict["follow_after_adjust"])
                    follow_before_adjust_values.append(score_dict["follow_before_adjust"])
                    after_adjust_content_correct_values.append(score_dict["after_adjust_content_correct"])
                except (json.JSONDecodeError, TypeError, KeyError):
                    print(f"Skipped invalid JSON entry: {score}")
                    continue

            if not follow_after_adjust_values or not follow_before_adjust_values or not after_adjust_content_correct_values:
                continue

            try:
                follow_after_adjust_mode = statistics.mode(follow_after_adjust_values)
                follow_before_adjust_mode = statistics.mode(follow_before_adjust_values)
                after_adjust_content_correct_mode = statistics.mode(after_adjust_content_correct_values)
            except statistics.StatisticsError:
                # If there is no unique mode, skip this entry
                continue

            # IAR: Whether the corrected instruction was successfully executed
            iar_values.append(1 if follow_after_adjust_mode == "YES" and after_adjust_content_correct_mode == "YES" else 0)
            # ECR: Whether the earlier instruction was identified as incorrect
            ecr_values.append(1 if follow_before_adjust_mode == "YES" else 0)

        iar = sum(iar_values) / len(iar_values) if iar_values else 0.0
        ecr = sum(ecr_values) / len(ecr_values) if ecr_values else 0.0

        print(f"IAR: {iar:.4f}")
        print(f"ECR: {ecr:.4f}")

        return iar, ecr





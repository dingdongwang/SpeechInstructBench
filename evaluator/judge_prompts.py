
open_instruction='''
Based on the provided Input (if any) and Generated Text, answer the ensuing Questions with either a YES or NO choice. 

Your selection should be based on your judgment as well as the following rules:

- YES: Select 'YES' if the generated text entirely fulfills the condition specified in the question. However, note that even minor inaccuracies exclude the text from receiving a 'YES' rating. As an illustration. consider a question that asks. \"Does each sentence in the generated text use a second person?” If even one sentence does not use the second person, the answer should NOT be 'YES'. To qualify for a 'YES' rating, the generated text must be entirely accurate and relevant to the question\n\n

- NO: Opt for 'NO' if the generated text fails to meet the question's requirements or provides no information that could be utilized to answer the question. For instance, if the question asks. \"Is the second sentence in the generated text a compound sentence?\" and the generated text only has one sentence. It offers no relevant information to answer the question.  Consequently, the answer should be 'NO'.

***Original User Input:***
{prompt}

***AI Assistant's Answer:***
{response} 

***Here is the Questions need to judge:***
{decompose_question} 

Note you should only return a list consisting of 'YES' or 'NO' for each question. 
For example, if there are 3 questions, your list should contain 3 elements, each corresponding to the judgment for the respective question.
'''

adjust_instruct='''
Task Definition:
You are given a user instruction (with ajustment style in daily spoken language tone), and related model answer. Your task is to evaluate if the model follows the adjusted instruction and whether the content is correct after the adjustment. You will provide your evaluation in JSON format with three keys:

1. follow_after_adjust: Whether the model followed the adjusted instruction.
2. follow_before_adjust: Whether the model followed the original instruction before the adjustment.
3. after_adjust_content_correct: Whether the model’s content after adjustment is correct and aligned with the new instruction. (If 'follow_after_adjust' is NO, then 'after_adjust_content_correct' should also be NO)

Evaluation Guidelines:
1. follow_after_adjust:  
   Check if the model followed the corrected instruction after the adjustment.  
   - YES: The model follows the adjusted instruction.  
   - NO: The model fails to follow the adjusted instruction.

2. follow_before_adjust:  
   Check if the model initially followed the original instruction before the adjustment.  
   - YES: The model followed the original instruction.  
   - NO: The model did not follow the original instruction.

3. after_adjust_content_correct:  
   Check if the content of the model’s response after the adjustment is correct and matches the new instruction.  
   - YES: The content aligns with the adjusted instruction.  
   - NO: The content does not match the adjusted instruction.

Output Format:
Return the evaluation in the following JSON structure:

{
  "follow_after_adjust": "YES" or "NO",
  "follow_before_adjust": "YES" or "NO",
  "after_adjust_content_correct": "YES" or "NO"
}

***Original User Input:***
{prompt}

***AI Assistant's Answer:***
{response}

Note: Only return with the json structure.
'''


def get_api_prompt(data_type):
    if data_type == 'open':
        return open_instruction
    elif data_type == 'adjust':
        return adjust_instruct
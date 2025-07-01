import json
import pandas as pd
import numpy as np
import re
import difflib

def merge_questions_setting(responses_2):
    question_df = pd.read_csv('C:\\Users\\1\\OneDrive\\Desktop\\feedback_pipeline\\question_id.csv')
    program_type = "stem"
    target_respondent = ['teacher', 'student']
    form_type = ['feedback', 'feedback competition']


    question_df = question_df[(question_df['program_type'] == program_type) & (question_df['form_type'].isin(form_type)) & (question_df['target_respondent'].isin(target_respondent))]

    question_id_mapping = {}

    for response_question in responses_2['question']:
        # Find the closest match in the question_types df
        closest_match = difflib.get_close_matches(
            response_question,                      # The question from responses_2
            question_df['question'],             # The list of questions in question_types
            n=1,                                    # Get only the top match
            cutoff=0.9                              # Minimum similarity ratio
        )

        # If a closest match is found, get its question_id from question_types
        if closest_match:
            match = closest_match[0]
            # Directly fetch the question_id from the question_types DataFrame
            question_id = question_df[question_df['question'] == match]['question_id'].values[0]
            question_id_mapping[response_question] = question_id
        else:
            # If no match is found, set as None
            question_id_mapping[response_question] = None

    # Map the question_id to the responses DataFrame, by adding the column 'question_id'
    responses_2['question_id'] = responses_2['question'].map(question_id_mapping)


    return responses_2, question_id_mapping



#for question, question_id in question_id_mapping.items():
  #if question_id is None:
    #print(f"Question: {question}, Question ID: {question_id}")
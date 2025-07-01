import json
import pandas as pd
import numpy as np
import re
import difflib
import ast 
import uuid

def clean_responses(responses):
  responses = responses.rename(columns = {'student_name':'name',
                                        'student_email':'email'})
  

  def convert_to_int(value):
    try:
      return int(value)
    except (ValueError, TypeError):
      if "⭐" in value:
        return value.count("⭐")
      else:
        return None
    

  responses['timestamp'] = pd.to_datetime(responses['feedback_completion_datetime'])
  responses['date'] = responses['timestamp'].dt.date

  responses_2 = []

  for idx, row in responses.iterrows():
    feedback_answers = row['feedback_form_answers']

    if isinstance(feedback_answers, str):
      try:
        feedback_answers = ast.literal_eval(feedback_answers)
      except Exception as e:
        print(f"Row {idx} parsing error: {e}")
        continue

    for item in feedback_answers:
      question = item.get('question', '').strip()
      response = item.get('answer', '').strip()

      # skip sections like "Part A" etc
      if 'Part' in question:
        continue

      if '.' in question:
        question = question.split('.', 1)[1].strip()

      # Extract response_int here
      if re.match(r'^\d+=', response):
        split_response = response.split("=")[0].strip()
        response_int = int(split_response)
      else:
        response = response.replace('\u2b50', '⭐')
        response_int = convert_to_int(response) # Fallback to original conversion


      responses_2.append({
      'name': row['name'],
      'question': question,
      'response': response,
      'response_int': response_int,
      })

  responses_2 = pd.DataFrame(responses_2)
  responses_2 = responses_2.merge(responses[[
      'id',
      'class_id',
      'class_name',
      'name',
      'email',
      'course_id',
      'course_name',
      'timestamp',
      'date']],
      on = 'name',
      how = 'left')
  
  return responses_2


#print ('responses are cleaned')


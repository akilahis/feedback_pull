import json
import pandas as pd
import re
import difflib 
import ast

with open('data/most_recent.json', 'r') as f:
    data = json.load(f)

responses = pd.DataFrame(data)
print('data is converted')

responses = responses.rename(columns = {'student_name':'name',
                                        'student_email':'email'

})
#define control
program_type = "stem"
target_respondent = ['teacher', 'student']
form_type = ['feedback', 'feedback competition']

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

print('Responses are cleaned')
question_df = pd.read_csv('C:\\Users\\1\\OneDrive\\Desktop\\feedback_pipeline\\question_id.csv')

# Determine form_type based on whether course_name contains "Competition"

#if any("competition" in str(name).lower() for name in responses_2['course_name'].unique()):
        #form_type = ['feedback competition']
#else:
        #form_type = ['feedback']

question_df = question_df[(question_df['form_type'].isin(form_type)) & (question_df['target_respondent'].isin(target_respondent))]
#Iterate through the questions in the responses_2 df
question_id_mapping = {}

for response_question in responses_2['question']:
    # Find the closest match in the question_types df
    closest_match = difflib.get_close_matches(
        response_question,                      # The question from responses_2
        question_df['question'],             # The list of questions in question_types
        n=1,                                    # Get only the top match
        cutoff=0.8                              # Minimum similarity ratio
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

for question, question_id in question_id_mapping.items():
  if question_id is None:
    print(f"Question: {question}, Question ID: {question_id}")
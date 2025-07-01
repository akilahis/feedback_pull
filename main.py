import json
import pandas as pd
import numpy as np
import re
import difflib
import os

#create supabase client
from supabase import create_client, Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#load saved responses
with open('data/most_recent.json', 'r') as f:
    data = json.load(f)
responses = pd.DataFrame(data)

#start the scripts in sequence
from clean import clean_responses
from merge import merge_questions_setting
from export_supabase import export_into_supabase
import uuid


def main():
    #question_df = pd.read_csv('C:\\Users\\1\\OneDrive\\Desktop\\feedback_pipeline\\question_id.csv')
    responses_2 = clean_responses(responses)
    responses_2, question_id_mapping = merge_questions_setting(responses_2)
    # Export and insert data (only once)
    data_records = export_into_supabase(responses_2)

    #try:
        #response = supabase.table("sms_feedback_fact").insert(data_records).execute()
        #print("Response inserted successfully")
    #except Exception as e:
        #print("Error inserting data:", e)

    # Check for None question IDs (for debugging purposes)
    for question, question_id in question_id_mapping.items():
        if question_id is None:
            print(f"Question: {question}, Question ID: {question_id}")

if __name__ == "__main__":
    main()

#print(responses_2.info())
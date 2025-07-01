import numpy as np
import pandas as pd


def export_into_supabase(df):
    df = df.drop(columns=['class_name', 'course_name'])
    df = df.replace('', np.nan)
    df = df.replace({np.nan: None})
    df = df.replace([np.nan, pd.NA], None)
    null_indicators = ['N/A', 'NA', 'null', 'NULL', 'None', '', np.nan, pd.NA, pd.NaT]
    df = df.replace(null_indicators, None)
    df['timestamp'] = df['timestamp'].astype(str)
    df['date'] = df['date'].astype(str)
    df = df.dropna(subset=['response'])
    df['response_int'] = df['response_int'].replace({np.nan: None})


    data_records = df.to_dict(orient="records")
    return data_records


            





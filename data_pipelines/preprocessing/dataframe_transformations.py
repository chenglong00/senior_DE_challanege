import numpy as np
import re

# Define a dictionary of preprocessing rules
import pandas as pd
from common.constants import DATETIME_FORMAT, EMAIL_PATTERN
from common.utils import match_date_pattern, is_folder_exist, create_folder
from datetime import datetime
import hashlib
from pandas import DataFrame


################ Data Cleaning Functions ##################
def drop_na(df, cols) -> DataFrame:
    return df.dropna(subset=cols)


def split_first_last_name(df, col, delimiter=' ') -> DataFrame:
    df[['first_name', 'last_name']] = df[col].str.split(delimiter, n=1, expand=True)
    return df


def to_target_datetime_format(df, col, target_format) -> DataFrame:
    df[col] = pd.to_datetime(df[col].apply(lambda datetime_str: match_date_pattern(datetime_str)),
                             format=DATETIME_FORMAT).dt.strftime(target_format)
    return df


def generate_membership_id(df, last_name, birthday) -> DataFrame:
    # concatenate the last name and birthday in the format of YYYYMMDD
    df["str_to_hash"] = df[last_name] + "_" + df[birthday]

    df["truncated_hash"] = df["str_to_hash"].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest()[:5])

    df["membership_id"] = df[last_name] + "_" + df["truncated_hash"]

    return df


################ Data Validation Functions ##################
def is_valid_email(df, col, patterns=EMAIL_PATTERN) -> DataFrame:
    df["valid_email"] = df[col].apply(lambda x: True if re.search(patterns, x) else False)
    return df


def is_above_age(df, date_of_birth_col, threshold_age=18, reference_date=None) -> DataFrame:
    # calculate the age of each applicant
    if not reference_date:
        reference_date = datetime.now()
    else:
        reference_date = datetime.strptime(reference_date, DATETIME_FORMAT)
    df['age'] = (reference_date - pd.to_datetime(df[date_of_birth_col])).astype('timedelta64[Y]')

    # create the above_18 column based on the age
    df[f'above_{threshold_age}'] = df['age'] >= threshold_age

    return df


def is_valid_mobile(df, mobile_no_col, expected_len=8) -> DataFrame:
    # check mobile len
    df[mobile_no_col] = df[mobile_no_col].str.strip()
    df[mobile_no_col] = df[mobile_no_col].str.replace(' ', '')
    df[mobile_no_col] = df[mobile_no_col].str.replace('-', '')
    df['valid_mobile'] = df[mobile_no_col].str.len() == expected_len
    return df


def is_success_application(df):
    # calculate the age of each applicant
    df["success_application"] = df["valid_mobile"] & df["above_18"] & df["valid_email"]
    return df


def success_unsuccess_application_split(df):
    # calculate the age of each applicant
    expected_cols = ['first_name', 'last_name', 'email', 'mobile_no', 'age', 'membership_id']
    # df_success = df.loc[df["success_application"] == True, expected_cols].copy()
    # df_unsuccess = df.loc[df["success_application"] == False, expected_cols].copy()
    df_success = df[df["success_application"] == True][expected_cols].copy()
    df_unsuccess = df[df["success_application"] == False][expected_cols].copy()
    return df_success, df_unsuccess


def persist_processed_data(df, input_file_name, output_path, is_success):
    parent_dir = output_path
    success_output_folder = f"{parent_dir}/output/success"
    unsuccess_output_folder = f"{parent_dir}/output/unsuccess"

    for output_folder in [success_output_folder, unsuccess_output_folder]:
        if not is_folder_exist(output_folder):
            create_folder(output_folder)

    # Get the current timestamp as a string
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    input_file_name = input_file_name.split(".")[0]

    if is_success:
        file_name = f"{success_output_folder}/{input_file_name}_success_{timestamp_str}.csv"
    else:
        file_name = f"{unsuccess_output_folder}/{input_file_name}_unsuccess_{timestamp_str}.csv"

    df.to_csv(file_name, index=False)
    return file_name

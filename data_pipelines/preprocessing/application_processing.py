from data_pipelines.preprocessing.dataframe_transformations import split_first_last_name, to_target_datetime_format, drop_na, \
    is_above_age, generate_membership_id, is_valid_mobile, is_valid_email, is_success_application, \
    success_unsuccess_application_split, persist_processed_data
import logging
from common.utils import get_file_name_from_path, get_directory_from_path

logger = logging.getLogger(__name__)

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

class ApplicationProcessing:

    def __init__(self, input_dataframe: DataFrame, input_file_path):
        self.input_file_name = get_file_name_from_path(input_file_path)
        self.data_dir = get_directory_from_path(input_file_path)
        self.df = input_dataframe
        self.df_success = DataFrame()
        self.df_unsuccess = DataFrame()

    def data_cleaning(self):
        self.df = drop_na(self.df, ["name"])
        self.df = split_first_last_name(self.df, "name")
        self.df = to_target_datetime_format(self.df, "date_of_birth", "%Y%m%d")
        self.df = generate_membership_id(self.df, "last_name", "date_of_birth")

    def data_validation(self):
        self.df = is_above_age(self.df, "date_of_birth", 18, "2022-01-01")
        self.df = is_valid_mobile(self.df, "mobile_no", expected_len=8)
        self.df = is_valid_email(self.df, "email")
        self.df = is_success_application(self.df)

    def data_split(self):
        self.df_success, self.df_unsuccess = success_unsuccess_application_split(self.df)

    def data_persistent(self):
        success_file_path = ""
        unsuccess_file_path = ""
        if not self.df_success.empty:
            success_file_path = persist_processed_data(self.df_success, input_file_name=self.input_file_name,
                                                       output_path=self.data_dir, is_success=True)
        if not self.df_success.empty:
            unsuccess_file_path = persist_processed_data(self.df_unsuccess, input_file_name=self.input_file_name,
                                                         output_path=self.data_dir, is_success=False)
        return success_file_path, unsuccess_file_path

    def run(self):
        self.data_cleaning()
        self.data_validation()
        self.data_split()
        success_file_path, unsuccess_file_path = self.data_persistent()
        return success_file_path, unsuccess_file_path

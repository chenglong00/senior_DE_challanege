from typing import List
from pandas import DataFrame
from data_pipeline.data_preprocessing_functions import split_first_last_name, to_target_datetime_format, drop_na, \
    is_above_age, generate_membership_id, is_valid_mobile, is_valid_email, is_success_application, \
    success_unsuccess_application_split, persist_processed_data
import logging
from common.utils import get_file_name_from_path, get_directory_from_path

logger = logging.getLogger(__name__)


class DataPreprocessing:

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

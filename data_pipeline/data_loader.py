from common.utils import is_in_list, is_file_exist
from common.exceptions import DataPipelineOperationalException
from common.constants import ACCEPTABLE_FILE_TYPES
import pandas as pd
from pandas import DataFrame
from data_pipeline.data_loader_functions import load_csv_file, load_txt_file
from typing import List


class DataLoader:

    def __init__(self, input_file: str, input_file_type: str):
        if not is_file_exist(input_file):
            raise DataPipelineOperationalException(f"Input file doesn't exist: {input_file}")
        self.input_file = input_file

        if not is_in_list(input_file_type, ACCEPTABLE_FILE_TYPES):
            raise DataPipelineOperationalException(f"Input file type is not allowed: {input_file_type}")
        self.input_file_type = input_file_type.lower()

    def load_data(self) -> List[DataFrame]:

        if self.input_file_type == "csv":
            df = load_csv_file(self.input_file)
        elif self.input_file_type == "txt":
            df = load_txt_file(self.input_file)

        return df

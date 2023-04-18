import unittest
from data_pipelines.preprocessing.application_processing import ApplicationProcessing
from data_pipelines.loaders.application_data_loader import ApplicationDataLoader
from common.utils import get_current_path, is_file_exist
import logging

logger = logging.getLogger(__name__)


class DataPreprocessingTestCase(unittest.TestCase):

    def setUp(self) -> None:
        current_path = get_current_path()
        right_path = f"{current_path}/data/applications_dataset_1.csv"
        right_type = "csv"
        self._data_loader = ApplicationDataLoader(right_path, right_type)
        self._df = self._data_loader.load_data()
        self._data_preprocessing = ApplicationProcessing(self._df, right_path)

    def test_data_cleaning(self) -> None:
        self._data_preprocessing.data_cleaning()
        df = self._data_preprocessing.df
        print(df.head(5))
        print(df.columns)
        self.assertTrue(df[df["first_name"] == ""].empty)
        self.assertTrue(df[df["last_name"] == ""].empty)
        self.assertTrue(df[df["date_of_birth"] == "nana-na-na"].empty)

    def test_data_validation(self) -> None:
        self._data_preprocessing.data_cleaning()
        self._data_preprocessing.data_validation()

        df = self._data_preprocessing.df
        self.assertTrue(df[(df["above_18"] == True) & (df["age"] < 18)].empty)
        self.assertTrue(df[(df["valid_mobile"] == True) & (df["mobile_no"].str.len() != 8)].empty)
        self.assertTrue(df[(df["valid_email"] == False) & (df["email"].str.endswith(".com"))].empty)
        self.assertTrue(
            df[(df["success_application"] == False) & (df["above_18"] & df["valid_mobile"] & df["valid_email"])].empty)

    def test_data_split(self) -> None:
        self._data_preprocessing.data_cleaning()
        self._data_preprocessing.data_validation()
        self._data_preprocessing.data_split()

        df_success = self._data_preprocessing.df_success
        df_unsuccess = self._data_preprocessing.df_unsuccess
        self.assertTrue(df_success[(df_success["mobile_no"].str.len() != 8)].empty)
        self.assertTrue(df_success[~ (
                (df_success["email"].str.endswith(".com")) | (df_success["email"].str.endswith(".net")))].empty)
        self.assertTrue(df_success[df_success["age"] < 18].empty)

        self.assertTrue(df_success[(df_success["mobile_no"].str.len() != 8)].empty)

        self.assertTrue(df_unsuccess[(df_unsuccess["mobile_no"].str.len() == 8)
                                     & (df_unsuccess["email"].str.endswith(".com") | df_unsuccess["email"].str.endswith(
            ".et"))
                                     & (df_unsuccess["age"] >= 18)
                                     ].empty)

    def test_data_split(self) -> None:
        self._data_preprocessing.data_cleaning()
        self._data_preprocessing.data_validation()
        self._data_preprocessing.data_split()
        success_file_path, unsuccess_file_path = self._data_preprocessing.data_persistent()

        self.assertTrue(is_file_exist(success_file_path))
        self.assertTrue(is_file_exist(unsuccess_file_path))
import unittest
from data_pipeline.data_loader import DataLoader
from common.utils import get_current_path
from common.exceptions import DataPipelineOperationalException
import logging
from pandas import DataFrame

logger = logging.getLogger(__name__)


class DataLoaderTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.current_path = get_current_path()
        self.wrong_path = f"{self.current_path}/datas"
        self.wrong_file_type = "csvs"
        self.right_path = f"{self.current_path}/data/applications_dataset_1.csv"
        self.right_type = "csv"

    def test_data_loader_init(self) -> None:
        # right path
        self.assertIsInstance(DataLoader(self.right_path, self.right_type), DataLoader)

        # wrong path
        with self.assertRaises(DataPipelineOperationalException) as context:
            DataLoader(self.wrong_path, self.right_type)

        logger.debug(context.exception)
        self.assertTrue(f"Input file doesn't exist: {self.wrong_path}" in str(context.exception))

        # wrong file type
        with self.assertRaises(DataPipelineOperationalException) as context:
            DataLoader(self.right_path, self.wrong_file_type)

        logger.debug(context.exception)
        self.assertTrue(f"Input file type is not allowed: {self.wrong_file_type}" in str(context.exception))

    def test_load_data(self):
        data_loader = DataLoader(self.right_path, self.right_type)
        df = data_loader.load_data()

        self.assertIsInstance(df, DataFrame)
        self.assertTrue(not df.empty)

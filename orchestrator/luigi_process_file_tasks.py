import luigi
from data_pipeline.data_loader import DataLoader
from data_pipeline.data_preprocessing import DataPreprocessing
from common.exceptions import DataPipelineException
from luigi.target import FileSystemTarget, Target
from common.utils import get_current_path, is_completed, archive_file, get_directory_from_path, create_folder
import os


class ProcessFileTask(luigi.Task):
    """Task that generates data"""
    data_folder_path = luigi.Parameter()

    def run(self):
        # Process input files
        for file_name in os.listdir(self.data_folder_path):
            input_file = os.path.join(self.data_folder_path, file_name)

            if input_file.endswith(".csv"):
                input_file_type = "csv"
            elif input_file.endswith(".txt"):
                input_file_type = "txt"

            if os.path.isfile(input_file):
                data_folder = get_directory_from_path(input_file)
                archive_folder = os.path.join(data_folder, "archive")
                retry_folder = os.path.join(data_folder, "retry")
                create_folder(archive_folder)
                create_folder(retry_folder)
                try:
                    data_loader = DataLoader(input_file, input_file_type)
                    df = data_loader.load_data()
                    data_processing = DataPreprocessing(df, input_file)
                    success_file_path, unsuccess_file_path = data_processing.run()
                    if not is_completed(success_file_path, unsuccess_file_path):
                        archive_file(retry_folder, archive_folder)
                        raise DataPipelineException(f"Error, output file not found.")
                    else:
                        archive_file(input_file, archive_folder)
                except Exception as e:
                    raise DataPipelineException(f"critical error, require manual intervention. {e}")


if __name__ == '__main__':
    # Process file
    current_path = get_current_path()
    data_path = os.path.join(current_path, "..\data")
    process_file = ProcessFileTask(data_folder_path=data_path)
    process_file.run()

import luigi
from data_pipeline.data_loader import DataLoader
from data_pipeline.data_preprocessing import DataPreprocessing
from common.exceptions import DataPipelineException
from luigi.contrib.filesystem import FileSystemTarget, FileSystemEventMonitor
from common.utils import get_current_path, is_completed


class ProcessFileTask(luigi.Task):
    """Task that generates data"""
    input_file = luigi.Parameter()
    input_file_type = luigi.Parameter()

    def run(self):
        # Process input files
        try:
            data_loader = DataLoader(self.input_file, self.input_file_type)
            df = data_loader.load_data()
            data_processing = DataPreprocessing(df, self.input_file)
            success_file_path, unsuccess_file_path = data_processing.run()
            if not is_completed(success_file_path, unsuccess_file_path):
                raise DataPipelineException(f"Error, output file not found. {e}")
        except Exception as e:
            raise DataPipelineException(f"critical error, require manual intervention. {e}")


class FileMonitor(FileSystemEventMonitor):
    """File monitor that triggers tasks when new files are created"""

    def on_created(self, file_path):
        # Only process .txt files
        if file_path.endswith(".csv"):
            # Schedule the ProcessFile task to run with the new file as input
            self.register_dependency(ProcessFileTask(input_file=file_path, input_file_type="csv"))

        if file_path.endswith(".txt"):
            # Schedule the ProcessFile task to run with the new file as input
            self.register_dependency(ProcessFileTask(input_file=file_path, input_file_type="txt"))


if __name__ == '__main__':
    # Start the file monitor to watch the specified path
    current_path = get_current_path()
    monitor = FileMonitor(path=f'{current_path}/data')
    monitor.run()

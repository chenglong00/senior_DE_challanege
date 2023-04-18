from datetime import datetime, timedelta
from airflow.decorators import dag, task
import os
from data_pipelines.loaders import DataLoader
from data_pipelines.preprocessing.application_processing import ApplicationProcessing
from common.utils import is_completed, get_current_path
from common.exceptions import DataPipelineException
import glob

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 17),
    'email': ['chenglong.w1@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': timedelta(minutes=1)
}


@dag(
    dag_id='monitor_folder_for_file',
    default_args=default_args,
    catchup=False,
    description='Monitor folder for new file',
)
def ProcessFiles():
    @task(task_id="process_file")
    def process_file():
        base_path = get_current_path()
        data_path = os.path.join(base_path, "data")
        input_file_type = "csv"
        input_files = glob.glob(f'{data_path}/*.{input_file_type}')
        print(input_files)
        for input_file in input_files:
            if input_file:
                data_loader = DataLoader(input_file, input_file_type)
                df = data_loader.load_data()
                data_processing = ApplicationProcessing(df, input_file)
                success_file_path, unsuccess_file_path = data_processing.run()
                if not is_completed(success_file_path, unsuccess_file_path):
                    raise DataPipelineException(f"Error, output file not found. {e}")
            else:
                print('No files found in folder')

    process_file()


run_dag = ProcessFiles()

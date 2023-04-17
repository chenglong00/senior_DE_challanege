import os
import logging
from typing import List
from pathlib import Path
from common.constants import DATE_PATTERN_SLASH_Y_M_D, DATE_PATTERN_SLASH_D_M_Y, \
    DATE_PATTERN_DASH_D_M_Y, DATE_PATTERN_DASH_Y_M_D, DATE_PATTERN_DASH_M_D_Y, DATE_PATTERN_SLASH_M_D_Y, \
    DATE_PATTERN_SLASH_Y_D_M, DATE_PATTERN_DASH_Y_D_M
import re
import shutil

logger = logging.getLogger(__name__)


def create_folder(folder_path: str) -> None:
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
        logger.info(f'Folder created: {folder_path}')
    else:
        logger.info(f'Folder exists')


def get_file_name_from_path(file_path: str) -> str:
    return os.path.basename(file_path)


def get_directory_from_path(file_path: str) -> str:
    return os.path.dirname(file_path)


def is_file_exist(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    return False


def is_folder_exist(folder_path: str) -> bool:
    if os.path.isdir(folder_path):
        return True
    return False


def is_in_list(value: str, list_of_values: List[str]) -> bool:
    if value.lower() in list_of_values:
        return True
    return False


def list_files_in_dir(folder_path: str, file_type: str = None) -> List[str]:
    file_ls = os.listdir(folder_path)
    if file_type:
        file_ls = [folder_path + "/" + file for file in file_ls if file_type in file]
    return file_ls


def get_current_path() -> str:
    return str(Path.cwd())


def match_date_pattern(datetime_str):
    year = "nana"
    month = "na"
    day = "na"

    if "-" in datetime_str:
        if match := re.search(DATE_PATTERN_DASH_Y_M_D, datetime_str):
            year, month, day = match.group(0).split("-")

        elif match := re.search(DATE_PATTERN_DASH_Y_D_M, datetime_str):
            year, day, month = match.group(0).split("-")

        elif match := re.search(DATE_PATTERN_DASH_D_M_Y, datetime_str):
            day, month, year = match.group(0).split("-")

        elif match := re.search(DATE_PATTERN_DASH_M_D_Y, datetime_str):
            month, day, year = match.group(0).split("-")

    if "/" in datetime_str:

        if match := re.search(DATE_PATTERN_SLASH_M_D_Y, datetime_str):
            month, day, year = match.group(0).split("/")

        elif match := re.search(DATE_PATTERN_SLASH_D_M_Y, datetime_str):
            day, month, year = match.group(0).split("/")

        elif match := re.search(DATE_PATTERN_SLASH_Y_M_D, datetime_str):
            year, month, day = match.group(0).split("/")

        elif match := re.search(DATE_PATTERN_SLASH_Y_D_M, datetime_str):
            year, day, month = match.group(0).split("/")

    return f"{year}-{month}-{day}"


def persist_data(df, file_path):
    df.to_csv(file_path, index=False)


def is_completed(success_file_path, unsuccess_file_path):
    # if both file not empty
    if (success_file_path
            and is_file_exist(success_file_path)
            and unsuccess_file_path
            and is_file_exist(unsuccess_file_path)):
        return True
    # if success file is empty
    elif (not success_file_path
          and unsuccess_file_path
          and is_file_exist(unsuccess_file_path)):
        return True
    # if unsuccess file is empty
    elif (success_file_path
          and is_file_exist(success_file_path)
          and not unsuccess_file_path):
        return True

    return False


def archive_file(src_file, dst_dir):
    shutil.move(src_file, dst_dir)

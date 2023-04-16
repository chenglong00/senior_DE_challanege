import pandas as pd


def load_txt_file(file, header=0, delimiter='\t'):
    return pd.read_csv(file, header=header, delimiter=delimiter)


def load_csv_file(file, header=0):
    return load_txt_file(file, delimiter=',', header=header)

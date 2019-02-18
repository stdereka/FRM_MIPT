import pandas as pd
from io import StringIO


def read_dat_file(path: str, header: list):
    with open(path, 'r') as f:
        data = f.read()
        data = data.replace(',', '.')
        data = data.replace(' ', ',')
        data = data.replace(',\n', '\n')
        data = data[data.find('\n')+1:]
        data = data[data.find('\n') + 1:]
        data = ','.join(header) + '\n' + data
        df = pd.read_csv(StringIO(data))
        return df


def get_params_from_file_name(name: str):
    name = name[:name.rfind('.')]
    params = [float(p) for p in name.split('_')]
    return params

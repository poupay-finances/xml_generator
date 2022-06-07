import json
import random
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from cloud_s3 import create_file_in_bucket


def gerador(opcao: str):
    dataframe = DataFrame()
    cidades = get_cidades_dataframe()
    for _ in range(60_000):
        dataframe = pd.concat([dataframe, gerar(opcao, cidades)])
    create_file_local(dataframe, opcao)
    create_file_in_cloud(dataframe, opcao)


def gerar(opcao: str, cidades: DataFrame):
    regiao, producao = get_random_soja_regiao() if opcao == 'soja' else get_random_gado_regiao()
    cidades_da_regiao = cidades[cidades['regiao'] == regiao]
    cidade_escolhida = cidades_da_regiao.sample()
    cidade_escolhida['item'] = opcao
    cidade_escolhida['quantidade'] = producao
    cidade_escolhida['ano'] = random.randint(2000, 2020)
    print(cidade_escolhida)
    return cidade_escolhida


def get_cidades_dataframe() -> DataFrame:
    estados = get_estados()
    cidades = get_cidades(estados)
    return parse_list_to_dataframe(cidades)


def get_estados():
    f = open('./datas/estados.json', "r", encoding="utf8")
    return json.loads(f.read())['estados']


def get_cidades(estados: list):
    cidades = list()

    for estado in estados:
        for cidade in estado['cidades']:
            cidades.append({
                "nome": cidade,
                "uf": estado['sigla'],
                "estado": estado['nome'],
                "regiao": estado['regiao']
            })
    return cidades


def parse_list_to_dataframe(data):
    return pd.DataFrame(data)


def get_random_soja_regiao():
    random_number = random.uniform(0, 100)
    if random_number < 35.3:
        return 'Centro-Oeste', round(random.uniform(0.1, 12), 2)
    elif random_number < 57:
        return 'Norte', round(random.uniform(1, 8), 2)
    elif random_number < 72.8:
        return 'Sul', round(random.uniform(0.1, 6), 2)
    elif random_number < 92.1:
        return 'Nordeste', round(random.uniform(0.1, 3), 2)
    else:
        return 'Sudeste', round(random.uniform(0.0, 0.5), 2)


def get_random_gado_regiao():
    random_number = random.randint(0, 100)
    if random_number < 41.6:
        return 'Norte', round(random.uniform(500_000, 2_000_000))
    elif random_number < 77.4:
        return 'Centro-Oeste', round(random.uniform(500_000, 1_000_000))
    elif random_number < 84.4:
        return 'Sul', round(random.uniform(250_000, 750_000))
    elif random_number < 92.1:
        return 'Nordeste', round(random.uniform(100_000, 300_000))
    else:
        return 'Sudeste', round(random.uniform(5_000, 50_000))


def create_file_local(dataframe: DataFrame, opcao: str):
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    dataframe.to_xml(path_or_buffer=f"./files/file_{now}_{opcao}.xml")


def create_file_in_cloud(dataframe: DataFrame, opcao: str):
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    content = dataframe.to_xml()
    create_file_in_bucket(content, f"dados-brutos/{opcao}_xml/file_{now}_{opcao}.xml")

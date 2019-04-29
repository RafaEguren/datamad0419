import pandas as pd
import numpy as np
import json
import requests

def acquire():
    cars = pd.read_csv('./data.csv', sep=';')
    return cars

def wrangle(df):
    cars1 = cars.drop_duplicates()
    cars1 = cars[['make', 'model', 'months_old', 'power','gear_type','fuel_type','kms','price']]
    cars1['old_years'] = cars1['months_old'].divide(12).round()
    cars1 = cars1[['make', 'model', 'power','gear_type','fuel_type','kms','old_years','price']]
    cars1['model'] = cars1['model'].str.replace('C-Elys�e', 'C-Elys')
    return cars1

def acquire2():
    response = requests.get('https://parallelum.com.br/fipe/api/v1/carros/marcas')
    results = response.json()
    return results

def wrangle2(df):
    datacars = pd.DataFrame(results)
    datacars.rename(columns={'nome': 'make'}, inplace=True)
    datacars['make'] = datacars['make'].str.replace('Alfa Romeo', 'Alfa')
    return datacars
 
def analyze(df):
    s1 = pd.merge(cars1,datacars,how='left', on=['make'])
    table = pd.pivot_table(s1, index=['make','codigo','model'], aggfunc={'model':[len],'power': np.mean, 'kms':np.mean, 'old_years':np.mean, 'price':np.mean}).round()
    return table

def report(df):
    table1 = table[['model','kms','power','old_years','price']]
    return table1.head()

#if __name__ == '__main__':

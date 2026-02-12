# %%
import pandas as pd
import datetime as dt 
import os

class Transform: 
     # read data json file
    def __init__(self):
        self.__df = pd.read_json('/home/vinicyos/python_projetos/monitoramento_preco/data/products.jsonl', lines=True)
    
    def execute(self):
        # transformations here, astype to convert data types
        self.__df['currentPrice'] = self.__df['currentPrice'].astype(float)
        self.__df['oldPrice'] = self.__df['oldPrice'].astype(float)

        # separate rating into two columns: rating_score and rating_count_sales
        newColumns = self.__df['rating'].str.split("de 5 estrelas." , n=1, expand=True)
        self.__df['rating_score'] = newColumns[0]
        self.__df['rating_count_sales'] = newColumns[1]

        # clean rating_score word Classificação and type cast to float
        self.__df['rating_score'] = self.__df['rating_score'].str.replace('Classificação', '')

        # clean rating_count_sales final point
        self.__df['rating_count_sales'] = self.__df['rating_count_sales'].str.replace('.' , '')

        # Store with null change by default value "Loja não informada"
        self.__df['store'] = self.__df['store'].fillna('Loja não informada')

        # oldPrice with null change by default currentPrice value
        self.__df['oldPrice'] = self.__df['oldPrice'].fillna(self.__df['currentPrice'])

        # rating count sales, rating score with null change by default value N/A
        self.__df['rating_count_sales'] = self.__df['rating_count_sales'].fillna('Não informado')
        self.__df['rating_score'] = self.__df['rating_score'].fillna('Não informado')

        contains_not_informed = self.__df['rating_count_sales'].str.contains('Não informado').any()
        if contains_not_informed: 
            # remove rows with rating_count_sales == 'Não informado'
            self.__df = self.__df.drop(self.__df[self.__df['rating_count_sales'] == 'Não informado'].index)
            self.__df = self.__df.reset_index(drop=True)

        self.__df['rating_score'] = self.__df['rating_score'].astype(float)
                    
        # removing point price
        self.__df['currentPrice'] = self.__df['currentPrice'].astype(str).str.replace('.' , '')
        self.__df['oldPrice'] = self.__df['oldPrice'].astype(str).str.replace('.' , '')
        # cast to float
        self.__df['currentPrice'] = pd.to_numeric(self.__df['currentPrice'], errors='coerce')
        self.__df['oldPrice'] = pd.to_numeric(self.__df['oldPrice'], errors='coerce')

        print(self.__df.info())

        # drop rating column
        self.__df = self.__df.drop(columns=['rating'])

        # create colum date with analysis 
        self.__df['date'] = dt.datetime.now().strftime('%d/%m/%Y')

        file_path = '../../data/products.csv'
        if(os.path.isfile(file_path)): 
            print("Arquivo existente")
            self.__df.to_csv('/home/vinicyos/python_projetos/monitoramento_preco/data/products.csv', index=False, mode='a', header=False)
        else: 
            print("Arquivo nao existente")
            self.__df.to_csv('/home/vinicyos/python_projetos/monitoramento_preco/data/products.csv', index=False)








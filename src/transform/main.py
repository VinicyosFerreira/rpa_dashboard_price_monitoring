# %%
import pandas as pd
import datetime as dt 

 # read data json file
df = pd.read_json('/home/vinicyos/python_projetos/monitoramento_preco/data/products.jsonl', lines=True)

# transformations here, astype to convert data types
df['currentPrice'] = df['currentPrice'].astype(float)
df['oldPrice'] = df['oldPrice'].astype(float)

# separate rating into two columns: rating_score and rating_count_sales
newColumns = df['rating'].str.split("de 5 estrelas." , n=1, expand=True)
df['rating_score'] = newColumns[0]
df['rating_count_sales'] = newColumns[1]

# clean rating_score word Classificação and type cast to float
df['rating_score'] = df['rating_score'].str.replace('Classificação', '')

# clean rating_count_sales final point
df['rating_count_sales'] = df['rating_count_sales'].str.replace('.' , '')

# Store with null change by default value "Loja não informada"
df['store'] = df['store'].fillna('Loja não informada')

# oldPrice with null change by default currentPrice value
df['oldPrice'] = df['oldPrice'].fillna(df['currentPrice'])

# rating count sales, rating score with null change by default value N/A
df['rating_count_sales'] = df['rating_count_sales'].fillna('Não informado')
df['rating_score'] = df['rating_score'].fillna('Não informado')

contains_not_informed = df['rating_count_sales'].str.contains('Não informado').any()
if contains_not_informed: 
    # remove rows with rating_count_sales == 'Não informado'
    df = df.drop(df[df['rating_count_sales'] == 'Não informado'].index)
    df = df.reset_index(drop=True)

df['rating_score'] = df['rating_score'].astype(float)
            
# removing point price
df['currentPrice'] = df['currentPrice'].astype(str).str.replace('.' , '')
df['oldPrice'] = df['oldPrice'].astype(str).str.replace('.' , '')
# cast to float
df['currentPrice'] = pd.to_numeric(df['currentPrice'], errors='coerce')
df['oldPrice'] = pd.to_numeric(df['oldPrice'], errors='coerce')

print(df.info())

# drop rating column
df = df.drop(columns=['rating'])

# create colum date with analysis 
df['date'] = dt.datetime.now().strftime('%d/%m/%Y')

df.to_csv('/home/vinicyos/python_projetos/monitoramento_preco/data/products.csv', index=False)








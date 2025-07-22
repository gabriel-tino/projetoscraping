import pandas as pd
import sqlite3
from datetime import datetime
df = pd.read_json('data\data.jsonl', lines=True)

df['_source'] = "https://www.amazon.com.br/s?k=tenis+corrida+masculino"
df['_datetime'] = datetime.now()

df['price'] = df['price'].astype(str).str.replace('.', '', regex=False)

df['price'] = df['price'].astype(float)

print(df)

conn = sqlite3.connect('data/amazonbrasil.sql')

df.to_sql('tenis', conn, if_exists='replace', index=False)

conn.close()
import http.client
import json
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

#data extraction

def extract_prices():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5hqygBScH1ifb1p6OdZodL:6uYLDoWQxkYaI5r4oHoxvr"
        }

    conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    data_string = data.decode("utf-8")
    data_list = json.loads(data_string)
    return data_list


#data transformation

def transform_prices(data_list):
    city_level = data_list['result']['cities']
    city_df = pd.DataFrame(city_level)
    city_df = city_df.drop(columns=['lowername'])
    city_df =city_df.rename(columns={'name': 'cities'})
    return city_df

#data loading

def load_prices(city_df):

    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')

    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

    with engine.connect() as conn:
        resort = conn.execute(text('select * from cities;'))
        for i in resort:
            print(i)

    city_df.to_sql('cities', engine , if_exists='replace',index=False )

  
def main():
    data_list=extract_prices()
    city_df = transform_prices(data_list)
    load_prices(city_df)
 
    print('ETL process completed successfully.')


    if __name__ == "__main__":
        main()
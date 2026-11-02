
import pandas as pd


def transform_prices(data_list):
    city_level = data_list['result']['cities']
    city_df = pd.DataFrame(city_level)
    city_df = city_df.drop(columns=['lowername'])
    city_df =city_df.rename(columns={'name': 'cities'})
    return city_df













from extract import extract_prices
from load import load_prices
from transform import transform_prices


def main():
    data_list = extract_prices()
    city_df = transform_prices(data_list)
    load_prices(city_df)

    print("ETL process completed successfully.")


if __name__ == "__main__":
    main()

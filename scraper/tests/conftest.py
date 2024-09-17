import pytest
import pandas as pd


@pytest.fixture()
def create_df():
    def _create_df(csv_filename):
        df = pd.read_csv(csv_filename)
        return df

    return _create_df


@pytest.fixture()
def hotel_cleaned_df(create_df):
    df = create_df(csv_filename="./data/hotels_cleaned_sample.csv")
    return df


@pytest.fixture()
def hotel_uncleaned_df(create_df):
    df = create_df(csv_filename="./data/hotels_uncleaned_sample.csv")
    return df

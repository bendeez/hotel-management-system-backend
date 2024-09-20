import pandas as pd
from hotel_data.data_cleaner.hotel_data_cleaner import clean_hotel_data
from constants import HotelCsvFiles

df = pd.read_csv(HotelCsvFiles.DEVELOPMENT_UNCLEANED.value)
df = clean_hotel_data(df=df)
df.to_csv(HotelCsvFiles.DEVELOPMENT_CLEANED.value, index=False)

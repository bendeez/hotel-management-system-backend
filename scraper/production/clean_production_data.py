from hotel_data.data_cleaner.hotel_data_cleaner import clean_hotel_data
import pandas as pd
from constants import HotelCsvFiles

df = pd.read_csv(HotelCsvFiles.PRODUCTION_UNCLEANED.value)
df = clean_hotel_data(df=df)
df.to_csv(HotelCsvFiles.PRODUCTION_CLEANED.value, index=False)

import pandas as pd
import asyncio
from hotel_data.hotel_data_to_database import sync_hotel_data_to_database
from constants import HotelCsvFiles


df = pd.read_csv(HotelCsvFiles.PRODUCTION_CLEANED.value)
asyncio.run(sync_hotel_data_to_database(df=df))

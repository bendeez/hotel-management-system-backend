import pandas as pd
import asyncio
from hotel_data.hotel_data_to_database import HotelDataSyncer
from constants import HotelCsvFiles
from hotel_data.data_cleaner.hotel_data_cleaner import serialize_df

df = pd.read_csv(HotelCsvFiles.PRODUCTION_CLEANED.value)
df = serialize_df(df=df)

hotel_data_syncer = HotelDataSyncer(task_count=3)
asyncio.run(hotel_data_syncer.sync_hotel_data_to_database(df=df))

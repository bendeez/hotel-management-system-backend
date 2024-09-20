import pandas as pd
from constants import HotelCsvFiles

df = pd.read_csv(HotelCsvFiles.PRODUCTION_CLEANED.value)
print(df)

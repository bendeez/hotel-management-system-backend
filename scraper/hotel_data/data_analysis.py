# import pandas as pd
# from constants import HotelCsvFiles
# from hotel_data.data_cleaner.hotel_data_cleaner import serialize_df
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# sns.displot(data, kde=True, bins=15)
#
# df = pd.read_csv(HotelCsvFiles.PRODUCTION_CLEANED.value)
# df = serialize_df(df=df)
# df.interpolate(inplace=True)
# train, test = train_test_split(df, test_size=0.2, random_state=42)
# train.interpolate(inplace=True)
# plt.hist(train["rating_out_of_10"], bins=10)
# plt.show()

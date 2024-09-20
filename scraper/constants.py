from enum import Enum


class HotelCsvFiles(Enum):
    PRODUCTION_CLEANED = "./production/data/hotels_cleaned_production_copy.csv"
    PRODUCTION_UNCLEANED = "./production/data/hotels_uncleaned_production_copy.csv"
    DEVELOPMENT_CLEANED = "./development/data/hotels_cleaned_sample.csv"
    DEVELOPMENT_UNCLEANED = "./development/data/hotels_uncleaned_sample.csv"

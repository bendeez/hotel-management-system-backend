import ast
import re


class HotelCleanDataTool:
    def safe_literal_eval(self, value):
        try:
            return ast.literal_eval(value)
        except Exception as e:
            return None

    def modify_amenities(self, amenity):
        try:
            return [a.strip() for a in amenity if a != ""]
        except Exception as e:
            return None

    def modify_classified_ratings(self, review):
        try:
            return {key: float(value) for key, value in review.items()}
        except Exception as e:
            return None

    def modify_starting_price(self, price):
        try:
            return float(price.replace("$", "").replace(",", ""))
        except Exception as e:
            return None

    def modify_num_of_reviews(self, review):
        try:
            return int(review.split(" ")[0].replace(",", ""))
        except Exception as e:
            return None

    def modify_num_rating(self, rating):
        try:
            return float(rating.split(" ")[1])
        except Exception as e:
            return None

    def get_rid_of_newline_characters(self, value):
        try:
            return re.sub(r"(\\n)+", " | ", value)
        except Exception as e:
            return None

    def modify_room_to_price(self, rooms):
        """
            safe_literal_eval could return none leading to a NoneType has no attribute "items"
            error
        :param rooms:
        :return:
        """
        try:
            return [
                {
                    key: [v.strip() for v in value.split("|") if v not in [" ", ""]]
                    for key, value in self.safe_literal_eval(repr(room)).items()
                }
                for room in rooms
            ]
        except Exception as e:
            return None

    def get_unique_values(self, value):
        if isinstance(value, list):
            return list(set(value))
        else:
            return None


ht = HotelCleanDataTool()

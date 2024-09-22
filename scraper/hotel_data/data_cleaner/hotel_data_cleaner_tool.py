import ast
import re


class HotelCleanDataTool:
    def safe_literal_eval(self, value):
        try:
            return ast.literal_eval(value)
        except Exception as e:
            print(e)
            return None

    def modify_amenities(self, amenity):
        try:
            return [a.strip() for a in amenity if a != ""]
        except Exception as e:
            print(e)
            return None

    def modify_classified_ratings(self, review):
        try:
            return {key: float(value) for key, value in review.items()}
        except Exception as e:
            print(e)
            return None

    def modify_starting_price(self, price):
        try:
            return float(price.replace("$", "").replace(",", ""))
        except Exception as e:
            print(e)
            return None

    def modify_house_rules(self, house_rules):
        if isinstance(house_rules, dict):
            for key, value in house_rules.copy().items():
                if key == "Cards accepted at this property":
                    house_rules["Cards accepted at this hotel"] = value
                    del house_rules[key]
                elif key == "Parties":
                    house_rules["Groups"] = value
                    del house_rules[key]
                elif key == "No age restriction":
                    house_rules["Age restriction"] = value
                    del house_rules[key]
            return house_rules

        else:
            return None

    def modify_num_of_reviews(self, review):
        try:
            return int(review.split(" ")[0].replace(",", ""))
        except Exception as e:
            print(e)
            return None

    def modify_num_rating(self, rating):
        try:
            return float(rating.split(" ")[1])
        except Exception as e:
            print(e)
            return None

    def get_rid_of_newline_characters(self, value):
        try:
            return re.sub(r"(\\n)+", " | ", value)
        except Exception as e:
            print(e)
            return None

    def modify_room_to_price(self, rooms):
        """
            safe_literal_eval could return none leading to a NoneType has no attribute "items"
            error
        :param rooms:
        :return:
        """
        try:
            modified_rooms = [
                {
                    key: [v.strip() for v in value.split("|") if v not in [" ", ""]]
                    for key, value in self.safe_literal_eval(repr(room)).items()
                }
                for room in rooms
            ]
            rooms_with_num_columns = [
                self.add_columns_to_room(room=room) for room in modified_rooms
            ]
            return rooms_with_num_columns
        except Exception as e:
            print(e)
            return None

    def get_unique_values(self, value):
        if isinstance(value, list):
            return list(set(value))
        else:
            return None

    def add_new_guest_count_columns(self, room: dict):
        guest_count = " ".join(room["guest_count"])
        guest_count = re.findall(r"Max. people: \d+", guest_count)
        if guest_count:
            guest_count = guest_count[0]
            guest_count = int(guest_count.strip().split(" ")[-1])
            room["num_guest_count"] = guest_count
        return room

    def add_new_price_columns(self, room: dict):
        price = " ".join(room["price"])
        price = re.findall(r"(?i)price.*\$\d+", price)
        if price:
            price_and_fee = price[0].split("+")
            if price_and_fee:
                price_wo_fee = float(
                    price_and_fee[0]
                    .strip()
                    .split(" ")[-1]
                    .replace("$", "")
                    .replace(",", "")
                )
                if len(price_and_fee) == 2:
                    tax_and_fee = float(price_and_fee[1].strip().replace("$", ""))
                    room["num_tax_and_fee"] = tax_and_fee
                room["num_price"] = price_wo_fee
        return room

    def add_columns_to_room(self, room: dict):
        try:
            room = self.add_new_guest_count_columns(room=room)
            room = self.add_new_price_columns(room=room)
            return room
        except Exception as e:
            print(e)
            return None


ht = HotelCleanDataTool()

#!/usr/bin/python3
from base_model import BaseModel
from cities import Cities
from Persistance.data_management import DataManager as DM

class Country(BaseModel):
    def __init__(self, country_name):
        super().__init__()
        self.country_name = country_name
        self.cities = []

    def add_city(self, city):
        if isinstance(city, Cities) and city.city_name not in [c.city_name for c in self.cities]:
            self.cities.append(city)

    def get_cities(self):
        return self.cities

    def get_country_name(self):
        return self.country_name

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "country": self.country_name,
            "cities": [city.to_dict() for city in self.cities]
        })
        return base_dict
    
    

# Example Usage
# lesotho = Country("Lesotho")
# south_africa = Country("South Africa")

# city1 = Cities("Maseru", lesotho)
# city2 = Cities("Hlotse", lesotho)
# city3 = Cities("Pitseng", lesotho)

# lesotho.add_city(city1)
# lesotho.add_city(city2)
# lesotho.add_city(city3)

# city4 = Cities("Cape Town", south_africa)
# city5 = Cities("Durban", south_africa)
# city6 = Cities("East London", south_africa)

# south_africa.add_city(city4)
# south_africa.add_city(city5)
# south_africa.add_city(city6)

# dm = DM()
# dm.save("country", lesotho.to_dict(), None, "Lesotho")

# print(f"Country: {lesotho.get_country_name()}")
# print("Cities:")
# for city in lesotho.get_cities():
#     city_dict = city.to_dict()
#     print(f"- {city_dict['city_name']} (ID: {city_dict['id']}, Country: {city_dict['country']}, Created at: {city_dict['created_at']})")

# print(f"\nCountry: {south_africa.get_country_name()}")
# print("Cities:")
# for city in south_africa.get_cities():
#     city_dict = city.to_dict()
#     print(f"- {city_dict['city_name']} (ID: {city_dict['id']}, Country: {city_dict['country']}, Created at: {city_dict['created_at']})")

# # Print the dictionaries
# print("\nCountry Dictionary Lesotho:")
# print(lesotho.to_dict())

# print("\nCountry Dictionary South Africa:")
# print(south_africa.to_dict())
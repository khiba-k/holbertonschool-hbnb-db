from Persistance.interface import IPersistenceManager
from Model import base_model as bm
import json
import os


class DataManager(IPersistenceManager):
    """
    Class for data management
    """

    def __init__(self, file_path="data_file.json"):
        self.file_path = file_path
        # Ensure the file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({
                    "users": {},
                    "countries": {},
                    "reviews": {},
                    "places": [],
                    "amenities": [],
                    "emails": {}
                }, file, indent=4)

    def save(self, entity_type, data, host_id=None, entity_id=None, country_code=None, city_id=None):
        """
        Save data to JSON file.

        Args:
            entity_type (string): Type of entity.
            data (object): Dictionary storing information.
            host_id (string): ID of host.
            entity_id (string): ID of entity.
        """
        try:
            with open(self.file_path, "r+", encoding="utf-8") as file:
                file_data = json.load(file)

                if country_code:
                    if country_code in file_data["countries"]:
                        if city_id:
                            if city_id not in file_data["countries"][country_code]:
                                file_data["countries"][country_code][city_id] = data
                        else:
                            file_data["countries"][country_code] = data

                if host_id and entity_id:
                    if host_id not in file_data["users"]:
                        if entity_type == "users":
                            file_data["users"][host_id] = {}
                        else:
                            return "Host does not exist"
                    if entity_type == "users":
                        if entity_type not in file_data["users"][host_id]:
                            file_data["users"][host_id][entity_type] = {}
                        file_data["users"][host_id][entity_type][entity_id] = data
                    else:
                        file_data[entity_type][entity_id] = data
                elif entity_id:
                    file_data[entity_type][entity_id] = data
                else:
                    if entity_type in ["places", "amenities"]:
                        file_data[entity_type].append(data)

                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error saving data: {e}")

    def get(self, entity_type, entity_id=None, host_id=None, country_code=None, city_id=None):
        """
        Load information from data file.

        Args:
            entity_type (string): Type of entity (places, users, amenities, cities, or countries).
            entity_id (string): ID of places, users, amenities, cities, or countries.
            host_id (string): ID of host

        Returns:
            dict: Python dictionary of requested data.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if country_code:
                    if country_code in data["countries"]:
                        if city_id:
                            if city_id in data["countries"][country_code]:
                                return data["countries"][country_code][city_id]

                if host_id is not None:
                    if entity_type == "users":
                        if entity_type in data["users"][host_id]:
                            if entity_id is not None:
                                return data["users"][host_id][entity_type].get(entity_id)
                            return data["users"][host_id]
                    else:
                        return data[entity_type][entity_id]
                if entity_type in data:
                    if isinstance(data[entity_type], list) and entity_id is not None:
                        for item in data[entity_type]:
                            if item['id'] == entity_id:
                                return item
                    if entity_id is not None:
                        return data[entity_type].get(entity_id)
                    return data.get(entity_type)
                return None
        except IOError as e:
            print(f"Error loading data: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def update(self, entity_type, data, host_id=None, entity_id=None, country_code=None, city_id=None):
        """
        Update data in JSON file.

        Args:
            entity_type (string): Type of entity (places, users, amenities, cities, or countries).
            data (object): Dictionary storing updated information.
            host_id (string): ID of host.
            entity_id (string): ID of the entity to update.
        """
        stamps = bm.BaseModel()
        data["updated_at"] = stamps.updated_at

        if country_code:
            if country_code in file_data["countries"]:
                if city_id:
                    if city_id in file_data["countries"][country_code]:
                        file_data["countries"][country_code][city_id] = data

        try:
            with open(self.file_path, "r+", encoding="utf-8") as file:
                file_data = json.load(file)

                if host_id and entity_id:
                    if entity_type == "users":
                        if host_id not in file_data["users"]:
                            return "Host does not exist"
                        if entity_type not in file_data["users"][host_id]:
                            return "Entity does not exist"
                        if entity_id in file_data["users"][host_id][entity_type]:
                            file_data["users"][host_id][entity_type][entity_id] = data
                    else:
                        file_data[entity_type][entity_id] = data
                elif entity_id:
                    if entity_type in ["places", "amenities"]:
                        for i, item in enumerate(file_data[entity_type]):
                            if item.get("id") == entity_id:
                                file_data[entity_type][i] = data
                                break
                    elif entity_type in ["emails", "reviews", "countries"]:
                        file_data[entity_type][entity_id] = data
                else:
                    file_data[entity_type] = data

                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
        except (IOError, json.JSONDecodeError) as e:
            return f"Error updating data: {e}"
        return None

    def delete(self, entity_type, entity_id=None, host_id=None, country_code=None, city_id=None):
        """
        Delete information from JSON file.

        Args:
            entity_type (string): Type of entity (places, users, amenities, cities, or countries).
            entity_id (string): ID of the entity to delete.
            host_id (string): ID of host.
        """
        try:
            with open(self.file_path, "r+", encoding="utf-8") as file:
                file_data = json.load(file)

                if country_code:
                    if country_code in file_data["countries"]:
                        if city_id:
                            if city_id in file_data["countries"][country_code]:
                                del file_data["countries"][country_code][city_id]

                if host_id:
                    if entity_type == "users":
                        del file_data["users"][host_id][entity_type][entity_id]
                    else:
                        del file_data[entity_type][entity_id]
                else:
                    if "host_id" in file_data[entity_type][entity_id]:
                        host_id = file_data[entity_type][entity_id]["host_id"]
                        del file_data["users"][host_id][entity_type][entity_id]
                    else:
                        del file_data[entity_type][entity_id]

                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
            return {"deleted": entity_id}
        except (IOError, json.JSONDecodeError, KeyError) as e:
            return f"Error deleting data: {e}"

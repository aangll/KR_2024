import json

class MuseumInventory:
    def __init__(self, filename="museum_inventory.json"):
        self.filename = filename
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.inventory = json.load(file)
        except FileNotFoundError:
            self.inventory = {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.inventory, file, indent=4)

    def add_item(self, item_id, name, description, date_acquired, location):
        if item_id in self.inventory:
            print("Експонат із таким ID вже існує.")
        else:
            self.inventory[item_id] = {
                "name": name,
                "description": description,
                "date_acquired": date_acquired,
                "location": location
            }
            self.save_data()
            print("Експонат додано.")

    def view_item(self, item_id):
        item = self.inventory.get(item_id)
        if item:
            print(f"ID: {item_id}")
            for key, value in item.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("Експонат не знайдено.")

    def update_item(self, item_id, **kwargs):
        if item_id in self.inventory:
            for key, value in kwargs.items():
                if key in self.inventory[item_id]:
                    self.inventory[item_id][key] = value
            self.save_data()
            print("Інформацію про експонат оновлено.")
        else:
            print("Експонат не знайдено.")

    def delete_item(self, item_id):
        if item_id in self.inventory:
            del self.inventory[item_id]
            self.save_data()
            print("Експонат видалено.")
        else:
            print("Експонат не знайдено.")

    def list_items(self):
        if self.inventory:
            print("Список експонатів у музеї:")
            for item_id, details in self.inventory.items():
                print(f"ID: {item_id} - Назва: {details['name']}")
        else:
            print("Список експонатів порожній.")

# Приклад використання
inventory = MuseumInventory()
inventory.add_item("001", "Давня статуя", "Статуя з бронзи з IV століття до н.е.", "2022-01-15", "Зал 1")
inventory.add_item("002", "Картина", "Картина 18 століття невідомого художника", "2022-03-12", "Зал 2")
inventory.view_item("001")
inventory.update_item("002", name="Картина відомого художника")
inventory.delete_item("001")
inventory.list_items()

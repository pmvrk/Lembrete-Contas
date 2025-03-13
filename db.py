import json
import os
from datetime import datetime, date

class JsonManager:
    def __init__(self, path, key):
        """
        Base class for handling JSON file operations.
        Ensures that the directory for the JSON file exists.
        :param path: Path to the JSON file
        :param key: Key name for storing items in JSON
        """
        self.path = path
        self.key = key
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def read_json(self) -> dict:
        """
        Reads the JSON file and returns its data.
        If the file does not exist or has an invalid format, it returns an empty structure.
        """
        if not os.path.exists(self.path):
            return {self.key: {}}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if self.key not in data:
                    data[self.key] = {}
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {self.key: {}}

    def write_json(self, data: dict) -> None:
        """
        Writes data to the JSON file, ensuring proper indentation and encoding.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

class RegisteredBills(JsonManager):
    def __init__(self, path='db/registered_bills.json'):
        """
        Initializes the database manager with a given JSON file path.
        Ensures that the directory for the JSON file exists.
        """
        super().__init__(path, "registered_bills")

    def read_bills(self) -> list:
        """
        Returns the list of bills from the JSON file.
        """
        return self.read_json().get(self.key, {})


    def add_bill(self, name: str, value: float, due_day: int, monthly_bill: bool) -> list:
        """
        Adds a new bill to the JSON file.

        :param name: Name of the bill
        :param value: Amount of the bill
        :param due_day: Due date of the bill (day of the month)
        :param monthly_bill: Boolean indicating if it is a recurring bill
        :return: Updated list of bills
        """
        data = self.read_json()
        bills = data[self.key]

        # Generate a unique ID
        new_id = new_id = str(max(map(int, bills.keys()), default=0) + 1)

        # Create new bill
        new_bill = {
            "name": name,
            "value": value,
            "due_date": due_day,
            "monthly_bill": monthly_bill
        }

        data[self.key][new_id] = new_bill
        self.write_json(data)

        return data[self.key]


    def delete_bill(self, id_bill: str) -> bool:
        """
        Deletes a bill by its ID from the JSON file.

        :param id_bill: ID of the bill to be deleted
        :return: True if the bill was deleted, False if not found
        """
        data = self.read_json()
        bills = data[self.key]

        if id_bill not in bills:
            return False  # Bill ID not found

        del data[self.key][id_bill]

        self.write_json(data)

        return True


class PaidBills(JsonManager):
    def __init__(self, path='db/paid_bills.json'):
        """
        Initializes the database manager with a given JSON file path.
        Ensures that the directory for the JSON file exists.
        """
        super().__init__(path, "paid_bills")

    def read_paid_bills(self) -> dict:
        """
        Retrieves all paid bills and converts the payment_date back to a date object.
        """
        data = self.read_json()
        for bill_id, bill in data[self.key].items():
            try:
                bill["payment_date"] = datetime.strptime(bill["payment_date"], "%Y-%m-%d").date()
            except (ValueError, KeyError):
                bill["payment_date"] = None  # Avoid crashing if the date format is wrong
        return data[self.key]


    def pay_bill(self, id_bill: str, date_of_payment: date) -> dict:
        """
        Adds a record of a bill payment to the JSON file.
        """
        data = self.read_json()
        paid_bills = data[self.key]

        # Generate a unique ID
        new_id = str(max(map(int, paid_bills.keys()), default=0) + 1)

        # Create new paid bill
        new_paid_bill = {
            "id_bill": id_bill,
            "payment_date": date_of_payment.strftime("%Y-%m-%d")
        }

        data[self.key][new_id] = new_paid_bill
        self.write_json(data)

        return data[self.key]


    def delete_paid_bill(self, id_paid_bill: str) -> bool:
        """
        Deletes a bill payment record by its ID from the JSON file.
        """
        data = self.read_json()
        paid_bills = data[self.key]

        if id_paid_bill not in paid_bills:
            return False  # ID not found

        del data[self.key][id_paid_bill]
        self.write_json(data)

        return True

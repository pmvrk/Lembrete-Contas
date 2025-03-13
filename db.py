import json
import os
from datetime import datetime, date

class JsonManager:
    def __init__(self, path):
        """
        Base class for handling JSON file operations.
        Ensures that the directory for the JSON file exists.
        """
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def read_json(self) -> dict:
        """
        Reads the JSON file and returns its data.
        If the file does not exist or has an invalid format, it returns an empty structure.
        """
        if not os.path.exists(self.path):
            return {"bills": []}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"bills": []}

    def write_json(self, data: dict) -> None:
        """
        Writes data to the JSON file, ensuring proper indentation and encoding.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

class RegisteredBills(JsonManager):
    def __init__(self, path='db/bills.json'):
        """
        Initializes the database manager with a given JSON file path.
        Ensures that the directory for the JSON file exists.
        """
        super().__init__(path)

    def read_bills(self) -> list:
        """
        Returns the list of bills from the JSON file.
        """
        return self.read_json().get("bills", [])


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
        bills = data["bills"]

        # Generate a unique ID
        new_id = max((bill.get("bill_id", 0) for bill in bills), default=0) + 1

        # Create new bill
        new_bill = {
            "bill_id": new_id,
            "name": name,
            "value": value,
            "due_date": due_day,
            "monthly_bill": monthly_bill
        }

        data["bills"].append(new_bill)

        self.write_json(data)

        return data["bills"]


    def delete_bill(self, id_bill: int) -> bool:
        """
        Deletes a bill by its ID from the JSON file.

        :param bill_id: ID of the bill to be deleted
        :return: True if the bill was deleted, False if not found
        """
        data = self.read_json()
        bills = data["bills"]

        updated_bills = [bill for bill in bills if bill["bill_id"] != id_bill]

        if len(bills) == len(updated_bills):
            return False  # Bill ID not found

        data["bills"] = updated_bills
        self.write_json(data)

        return True


class PaidBills(JsonManager):
    def __init__(self, path='db/paid_bills.json'):
        """
        Initializes the database manager with a given JSON file path.
        Ensures that the directory for the JSON file exists.
        """
        super().__init__(path)

    def read_paid_bills(self) -> list:
        """
        Retrieves all paid bills and converts the due_date back to a date object.
        """
        data = self.read_json()
        for bill in data.get("bills", []):
            bill["payment_date"] = datetime.strptime(bill["payment_date"], "%Y-%m-%d").date()  # Convertendo string para date
        return data.get("bills", [])


    def pay_bill(self, id_bill:int, date_of_payment:date) -> None:
        """
        Adds a record of a bill payment to the JSON file.

        :param id_bill: id of the bill
        :param date_of_payment: date of the payment
        :return: None
        """
        data = self.read_json()
        paid_bills = data["bills"]

        # Generate a unique ID
        new_id = max((paid_bill.get("id_paid_bill", 0) for paid_bill in paid_bills), default=0) + 1

        # Create new bill
        new_paid_bill = {
            "id_paid_bill": new_id,
            "id_bill": id_bill,
            "payment_date": date_of_payment.strftime("%Y-%m-%d"),
        }

        data["bills"].append(new_paid_bill)
        self.write_json(data)

        return data["bills"]


    def delete_paid_bill(self, id_paid_bill: int) -> bool:
        """
        Deletes a bill payment record by its ID from the JSON file.

        :param id_paid_bill: ID of the bill payment record to be deleted
        :return: True if the bill was deleted, False if not found
        """
        data = self.read_json()
        paid_bills = data["bills"]

        updated_paid_bills = [paid_bill for paid_bill in paid_bills if paid_bill["id_paid_bill"] != id_paid_bill]

        if len(paid_bills) == len(updated_paid_bills):
            return False  # Bill ID not found

        data["bills"] = updated_paid_bills
        self.write_json(data)

        return True

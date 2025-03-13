from db import DBManager

db = DBManager()

db.add_bill('Boleto', 300, 10, False)
db.delete_bill(4)

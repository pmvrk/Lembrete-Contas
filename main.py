from db import RegisteredBills, PaidBills
from datetime import date

registered_bills_obj = RegisteredBills()
paid_bills_obj = PaidBills()

data = date.today()

registered_bills_obj.read_bills()

registered_bills_obj.add_bill("Boleto", 100, 10, False)

registered_bills_obj.delete_bill(6)

paid_bills_obj.read_paid_bills()

paid_bills_obj.pay_bill(5,data)

paid_bills_obj.delete_paid_bill("3")

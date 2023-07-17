import frappe
from durar_masagh_company.whatsapp import get_only_number, send_whatsapp_message


def send_good_morning_message():
    numbers = frappe.db.get_list('User', pluck='mobile_no')
    numbers = get_only_number(numbers)

    whatsapp_message_doc = frappe.get_doc('Whatsapp Message', 'Good Morning Message')

    send_whatsapp_message(to=numbers, body=whatsapp_message_doc.message)
    
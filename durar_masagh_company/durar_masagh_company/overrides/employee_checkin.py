import frappe
from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin


class CustomEmployeeCheckin(EmployeeCheckin):
    pass


@frappe.whitelist()
def get_current_user_data(user_id):
    return frappe.db.get_value('Employee', {'user_id': user_id}, 'name')


@frappe.whitelist()
def get_last_employee_checkin(doc):
    doc = eval(doc)
    try:
        employee_checkin = frappe.get_last_doc('Employee Checkin', filters={"employee": doc.get('employee') or get_current_user_data(frappe.session.user)})
        return employee_checkin
    except:
        return {}
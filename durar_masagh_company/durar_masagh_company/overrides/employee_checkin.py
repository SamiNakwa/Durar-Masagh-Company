import frappe
from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from frappe.utils import getdate
from datetime import datetime, timedelta


class CustomEmployeeCheckin(EmployeeCheckin):
    pass


@frappe.whitelist()
def get_current_user_data_and_shift(user_id):
    data = {'employee':False, 'shift_data':False}

    try:
        employee_doc =  frappe.get_doc('Employee', {'user_id': user_id})

        if employee_doc.default_shift:
            shift_type_doc = frappe.get_doc('Shift Type', employee_doc.default_shift)
            today_datetime = datetime.combine(getdate(), datetime.min.time())
            shift_start = today_datetime + shift_type_doc.start_time
            shift_end = today_datetime + shift_type_doc.end_time
            shift_actual_start = shift_start - timedelta(minutes=300)
            shift_actual_end = shift_end + timedelta(minutes=300)

            temp = {
                'shift_type':employee_doc.default_shift,
                'shift_start': shift_start,
                'shift_end': shift_end,
                'shift_actual_start': shift_actual_start,
                'shift_actual_end': shift_actual_end
            }
            data['employee'] = employee_doc.name
            data['shift_data'] = temp
            return data
        else:
            data['employee'] = employee_doc.name
            return data
    except:
        return data

@frappe.whitelist()
def get_last_employee_checkin(doc):
    doc = eval(doc)
    try:
        employee_checkin = frappe.get_last_doc('Employee Checkin', filters={"employee": doc.get('employee') or get_current_user_data(frappe.session.user)})
        return employee_checkin
    except:
        return {}
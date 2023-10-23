import frappe
from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from frappe.utils import getdate
from datetime import datetime, timedelta
import json
from frappe.utils import cint
from frappe import _


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
    doc = frappe._dict(json.loads(doc))
    try:
        employee_checkin = frappe.get_last_doc(
                                'Employee Checkin',
                                filters={
                                    "employee": doc.employee,
                                    "time": ['between', [getdate(), getdate()]]
                                }
                            )
        return employee_checkin
    except:
        return {}
    

@frappe.whitelist()
def add_log_based_on_employee_field(
	employee_field_value,
	timestamp,
	device_id=None,
	log_type=None,
	skip_auto_attendance=0,
	employee_fieldname="attendance_device_id",
):
	"""Finds the relevant Employee using the employee field value and creates a Employee Checkin.

	:param employee_field_value: The value to look for in employee field.
	:param timestamp: The timestamp of the Log. Currently expected in the following format as string: '2019-05-08 10:48:08.000000'
	:param device_id: (optional)Location / Device ID. A short string is expected.
	:param log_type: (optional)Direction of the Punch if available (IN/OUT).
	:param skip_auto_attendance: (optional)Skip auto attendance field will be set for this log(0/1).
	:param employee_fieldname: (Default: attendance_device_id)Name of the field in Employee DocType based on which employee lookup will happen.
	"""

	if not employee_field_value or not timestamp:
		frappe.throw(_("'employee_field_value' and 'timestamp' are required."))

	employee = frappe.db.get_values(
		"Employee",
		{employee_fieldname: employee_field_value},
		["name", "employee_name", employee_fieldname],
		as_dict=True,
	)
	if employee:
		employee = employee[0]
	else:
		frappe.throw(
			_("No Employee found for the given employee field value. '{}': {}").format(
				employee_fieldname, employee_field_value
			)
		)

	doc = frappe.new_doc("Employee Checkin")
	doc.employee = employee.name
	doc.employee_name = employee.employee_name
	doc.time = timestamp
	doc.device_id = device_id
	doc.log_type = get_log_type(employee.name, timestamp, log_type)
	if cint(skip_auto_attendance) == 1:
		doc.skip_auto_attendance = "1"
	doc.insert()

	return doc


def get_log_type(employee, timestamp, log_type):

    try:
        date = timestamp.split(' ')[0]
        existing_checkin = frappe.db.get_all(
                                                'Employee Checkin', 
                                                filters = {
                                                    "employee":employee,                                 
                                                    "time": ['between',[date, date]]
                                                },
                                                fields=['*'],
                                                order_by='time desc'

                                            )
        if existing_checkin:
            ch_data = existing_checkin[0]
            if ch_data.log_type == 'IN':
                return 'OUT'
            elif ch_data.log_type == 'OUT':
                return 'IN'
            else:
                return 'IN'
        else:
            return 'IN'
    except Exception as ex:
        frappe.log_error(str(ex), 'Employee Checkin Finding The Log Type Process')
        return None
        
          
     
     
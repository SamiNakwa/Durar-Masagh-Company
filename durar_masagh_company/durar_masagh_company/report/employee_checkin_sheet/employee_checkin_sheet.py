# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = get_columns(filters), get_datas(filters)
	return columns, data



def get_columns(filters=None):
	
	return [
		_("Date") + ":Date:100",
		_("First Check-In Time") + ":Time:150",
		_("Last Check-Out Time") + ":Time:150",
        _("Lunch Break") + ":Duration:100",
	    _("Shift Start Time") + ":Time:125",
	    _("Shift End Time") + ":Time:125",
	    _("Hour To Work") + ":Duration:100",
        _("Working Time") + ":Duration:100",
	    _("Over Time/Less Time") + ":Duration:100",
		_("Down Fall Time") + ":Duration:100"
	]


def get_datas(filters=None):


	db_filters = {
		'employee':filters.employee,
		'time': ['between', [filters.from_date, filters.to_date]]
	}
	checkin_data = frappe.db.get_all('Employee Checkin', filters=db_filters, fields=['*'], order_by='time asc')
	
	if not checkin_data:
		frappe.msgprint(f'There is no checkin data for this employee {filters.employee} for this dates from date {filters.from_date} & to date {filters.to_date}')
		return []
	
	structure_data = get_structure_data(checkin_data)
	data = []
	for key, value in structure_data.items():
		temp = []

		temp.append(key)

		frist_in, last_out, diff, = get_in_and_out_time(value)
		
		temp.append(frist_in)
		temp.append(last_out)
		temp.append(60*60)

		shift_start, shift_end = get_shift_time_data(value, filters.employee)
		temp.append(shift_start)
		temp.append(shift_end)

		hour_work = get_hour_work(shift_start,shift_end)
		temp.append(hour_work)
		temp.append(diff)

		over_time = get_over_time(diff,hour_work)
		temp.append(over_time)

		shift_start = ensure_timedelta(shift_start)
	

		dwon_fall_time = get_down_fall_time(shift_start,shift_end,frist_in,last_out)
		temp.append(dwon_fall_time)

		data.append(temp)

	return data

   
def ensure_timedelta(time_value):
    if isinstance(time_value, str):
        time_format = "%H:%M:%S"
        
        try:
            time_value = datetime.strptime(time_value, time_format) - datetime.strptime("00:00:00", time_format)
        except ValueError:
            time_value = None  
    elif isinstance(time_value, timedelta):
        pass
    else:
        time_value = None
    
    return time_value

def get_in_and_out_time(value):
	frist_in = value[0].get('time').strftime("%H:%M:%S")
	last_out = value[-1].get('time').strftime("%H:%M:%S")
	diff = (value[-1].get('time') - value[0].get('time')).total_seconds() - (60 * 60)


	return frist_in, last_out, diff,

def get_structure_data(checkin_data):

	data = {}
	for ec in checkin_data:
		if data.get(str(ec.get('time').date())):
			data.get(str(ec.get('time').date())).append(ec)
		else:
			data[str(ec.get('time').date())] = [ec]
	
	return data


def get_shift_time_data(checkin_data, employee):

	try:
		shift_start = checkin_data[0].get('shift_start').time()
		shift_start = timedelta(
								hours=shift_start.hour,
								minutes=shift_start.minute,
								seconds=shift_start.second
								)
		shift_end = checkin_data[0].get('shift_end').time()
		shift_end = timedelta(
								hours=shift_end.hour,
								minutes=shift_end.minute,
								seconds=shift_end.second
								)
	except:
		shift_doc = get_current_shift_details(employee)
		if shift_doc:
			shift_start, shift_end = shift_doc
		else:
			frappe.throw("There is no shift assigned for a employee")

	return shift_start, shift_end



def get_current_shift_details(employee):
	
	shift_type = frappe.db.get_value('Employee', employee, 'default_shift')
	
	if shift_type:
		shift_doc = frappe.db.get_value('Shift Type', shift_type, ['start_time', 'end_time'])
		return shift_doc
	else:
		return False
	

def get_hour_work(shift_start,shift_end):
		hour_work = shift_end - shift_start
		
		return hour_work.seconds - 3600

def get_over_time(diff,hour_work):
	over_time = diff - hour_work
	return over_time

def get_down_fall_time(shift_start, shift_end, frist_in, last_out):
	frist_in = ensure_timedelta(frist_in)
	last_out = ensure_timedelta(last_out)
	mg = timedelta()
	eg = timedelta()

	if shift_start < frist_in:
		mg = frist_in - shift_start

	if shift_end > last_out:
		eg = shift_end - last_out


	downf_fall_time = mg + eg
	return downf_fall_time.seconds
	
	
		





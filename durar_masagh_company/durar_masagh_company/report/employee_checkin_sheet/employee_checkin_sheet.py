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
        _("Working Time") + ":Duration:100",
	    _("Over Time") + ":Duration:100",
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

		first_in, last_out, diff, over_time = get_in_and_out_time(value)
		
		temp.append(first_in)
		temp.append(last_out)
		temp.append(60*60)

		shift_start, shift_end = get_shift_time_data(value)
		temp.append(shift_start)
		temp.append(shift_end)

		temp.append(diff)
		temp.append(over_time)

		data.append(temp)


	return data

def get_in_and_out_time(value):
	first_in = value[0].get('time').strftime("%H:%M:%S")
	last_out = value[-1].get('time').strftime("%H:%M:%S")
	diff = (value[-1].get('time') - value[0].get('time')).total_seconds() - (60 * 60)

	if diff < 0:
		diff = 0

	over_time = 0
	if diff > 8*(60*60):
		over_time = diff-8*(60*60)

	return first_in, last_out, diff, over_time

def get_structure_data(checkin_data):

	data = {}
	for ec in checkin_data:
		if data.get(str(ec.get('time').date())):
			data.get(str(ec.get('time').date())).append(ec)
		else:
			data[str(ec.get('time').date())] = [ec]
	
	return data


def get_shift_time_data(checkin_data):

	shift_start = checkin_data[0].get('shift_start')
	shift_end = checkin_data[0].get('shift_end')


	return shift_start, shift_end




	




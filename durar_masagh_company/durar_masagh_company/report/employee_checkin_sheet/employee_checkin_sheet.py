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
		_("Log In Time") + ":Time:100",
		_("First Checkin Time") + ":Time:200",
		_("Last Checkin Time") + ":Time:200",
        _("Lunch Break") + ":Duration:100",
        _("Working Time") + ":Duration:100",
	]


def get_datas(filters=None):


	db_filters = {
		'employee':filters.employee,
		'time': ['between', [filters.from_date, filters.to_date]]
	}
	checkin_data = frappe.db.get_all('Employee Checkin', filters=db_filters, fields=['*'], order_by='time asc')
	
	if not checkin_data:
		return [[]]
	
	structure_data = get_structure_data(checkin_data)
	data = []
	for key, value in structure_data.items():
		temp = []

		temp.append(key)
		temp.append(filters.log_in_time)

		first_in, last_out, diff = get_in_and_out_time(value)
		
		temp.append(first_in)
		temp.append(last_out)
		temp.append(60*60)
		temp.append(diff)

		data.append(temp)

	return data

def get_in_and_out_time(value):
	first_in = value[0].get('time').strftime("%H:%M:%S")
	last_out = value[-1].get('time').strftime("%H:%M:%S")

	diff = (value[-1].get('time') - value[0].get('time')).total_seconds() - (60 * 60)

	if diff < 0:
		diff = 0

	return first_in, last_out, diff

def get_structure_data(checkin_data):

	data = {}
	for ec in checkin_data:
		if data.get(str(ec.get('time').date())):
			data.get(str(ec.get('time').date())).append(ec)
		else:
			data[str(ec.get('time').date())] = [ec]
	
	return data



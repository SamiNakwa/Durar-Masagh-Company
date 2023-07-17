# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from datetime import datetime, time

def execute(filters=None):
	columns, data = get_columns(filters=filters), get_datas(filters=filters)
	return columns, data


def get_columns(filters=None):
		return [ 
			_("Date Time")+ ":Date  Time:100",
			_("Milage Difference ") + ":int:100",
			_('Ignition') + ":int:100"
		]


def get_datas(filters=None):
	st = str(time.min)
	et = str(time.max)

	start_time = str(filters.date) + " "+ st
	end_time = str(filters.date) + " " + et

	query_filters = {
		'vehicle':filters.vehicle,
		'track_date_time': ['between', [start_time, end_time]]
	}

	Vehicle_ideal_hours = frappe.db.get_list('Vehicle Arabitra Logs', filters=query_filters, fields=['track_date_time', 'distance', 'ignition'], order_by='track_date_time asc') 
	return get_vehicle_data(Vehicle_ideal_hours)





def get_vehicle_data(vehicle_log):

	data = []
	length = len(vehicle_log)
	for index in range(length-1):
		current_log = vehicle_log[index]
		next_log = vehicle_log[index+1]
		temp = []
		milage_difference  =  next_log.get('distance', 0) - current_log.get('distance', 0)

		temp.append(current_log.get('track_date_time'))
		temp.append(milage_difference)
		temp.append(current_log.get('ignition'))

		data.append(temp) 
	return data



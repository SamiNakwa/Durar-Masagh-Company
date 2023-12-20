# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import format_datetime, get_datetime




def execute(filters=None):
	
	columns, data = get_columns(filters), get_datas(filters)
	return columns, data


def get_columns(filters=None):

	return [
		{
			"label": _("Vehicle No"),
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"width": 150,
			# "align":"center"
		},
		{
			"label": _("Driver Name"),
			"fieldname": "driver_name",
			"fieldtype": "Data",
			"width": 250,
			# "align":"center"
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Data",
			"width": 200,
			# "align":"center"
		},
		{
			"label": _("Start Odometer"),
			"fieldname": "start_odometer",
			"fieldtype": "Int",
			"width": 150,
		},
		{
			"label": _("End Odometer"),
			"fieldname": "end_odometer",
			"fieldtype": "Int",
			"width": 150,
		},
		{
			"label": _("Distance Travelled(Kms)"),
			"fieldname": "distance_travelled",
			"fieldtype": "Int",
			"width": 200,
		}
	]


def get_datas(filters=None):

	if filters.branch:
		query_filters = {'branch':filters.branch}
	else:
		query_filters = {}

	vehicle_list = frappe.db.get_all('Vehicle',filters = query_filters, fields=['license_plate', 'employee','branch'])

	
	arabitra_logs = frappe.db.get_all('Vehicle Arabitra Logs',
								   filters = [
									    ['track_date_time', '>=', filters.from_datetime],
                                       ['track_date_time', '<', filters.to_datetime]
								   ],
								   fields = ['vehicle','track_date_time','distance'],
								   order_by = 'track_date_time asc'
								   )

	if not arabitra_logs:
		frappe.msgprint(f'No vehicle log data available for the selected date: <b>{filters.from_datetime}</b> to <b>{filters.to_datetime}</b>')

	structured_data = get_structured_data(arabitra_logs,)
	sort_data = sorted_data(vehicle_list)

	data = []
	for key in sort_data:
		temp = []
		temp.append(key.license_plate)

		temp.append(key.employee) 

		temp.append(key.branch)
		
		if get_vehicle_log_datas(structured_data, key) == None:
			end = None
			start = None
		else:
			end, start = get_vehicle_log_datas(structured_data, key)
		temp.append(end)
		temp.append(start)

		distance = get_distance(start, end)
		temp.append(distance)

		data.append(temp)
		
	return data


def get_structured_data(arabitra_logs):

	structured_data = {}
	for log in arabitra_logs:
		if structured_data.get(log.vehicle):
			structured_data.get(log.vehicle).append(log)
		else:
			structured_data[log.vehicle] = [log]

	return structured_data


def get_vehicle_log_datas(structured_data, key):

	for data in structured_data:
		if key.license_plate == data:			
			last_odometer = (structured_data.get(data)[0]).distance
			start_odometer = (structured_data.get(data)[-1]).distance
			return last_odometer, start_odometer
	
	return None

	
def get_distance(start, end):

	if  start == None and end == None:
		return None	
	else:
		distance_travelled = start - end
		return distance_travelled
	

def sorted_data(vehicle_list):

	sorted_data = sorted(vehicle_list, key=lambda x: x["branch"] if x["branch"] is not None else "", reverse=True)
	return sorted_data
	


		

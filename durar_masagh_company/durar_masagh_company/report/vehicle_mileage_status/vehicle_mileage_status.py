# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from durar_masagh_company.constant import MONTH_TO_NUMBER
from datetime import datetime
from durar_masagh_company.utility import get_sart_and_end_date_of_month

def execute(filters=None):
	columns, data = get_columns(filters=filters), get_datas(filters=filters)
	return columns, data


def get_columns(filters=None):
		return [ 
			_("Date")+ ":date:100",
			_("Kilo Meter") + ":int:100",
		]


def get_datas(filters=None):

	if filters.get("month"):
		month = MONTH_TO_NUMBER.get(filters.get('month'))
		year = datetime.now().year
		_from, to = get_sart_and_end_date_of_month(month=month, year=year)
		
	elif filters.get('from') and filters.get('to'):
		_from, to = filters.get('from'), filters.get('to')
	else:
		frappe.msgprint(msg='Please select <b>month</b> or <b>From</b> and <b>To</b>')
		return []

	
	query_filters = {
		'license_plate': filters.get('vehicle'),
		'date': ['between', [str(_from), str(to)]],

	}

	vehicle_log = frappe.db.get_list('Vehicle Log', filters=query_filters, fields=['date', 'last_odometer', 'odometer'], order_by='date asc')

	data = []

	for log in vehicle_log:
		temp = []
		kilo_meter = log.get('odometer', 0) - log.get('last_odometer', 0)

		temp.append(log.get('date'))
		temp.append(kilo_meter)

		data.append(temp)

		temp = []


	return data



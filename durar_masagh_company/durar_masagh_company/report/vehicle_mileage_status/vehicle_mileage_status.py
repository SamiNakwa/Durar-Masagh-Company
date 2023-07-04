# Copyright (c) 2023, Samiulla Nakwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(filters=filters), get_datas(filters=filters)
	return columns, data


def get_columns(filters=None):
		return [ 
			_("Date") ",+ ":date:100",
		_("Kilo Meter") + ":int:50",
		]
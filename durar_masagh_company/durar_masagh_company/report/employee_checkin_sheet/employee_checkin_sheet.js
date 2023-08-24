// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Checkin Sheet"] = {
	"filters": [
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 1
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: 'Today',
			reqd: 1
		}
	]
};

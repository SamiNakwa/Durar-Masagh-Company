// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Distance"] = {
	"filters": [
		// {
		// 	fieldname: "vehicle",
		// 	label: __("Vehicle"),
		// 	fieldtype: "Link",
		// 	options: "Vehicle",
		// 	reqd: 1
		// },
		// {
		// 	fieldname: "date",
		// 	label: __("Date"),
		// 	fieldtype: "Date",
		// 	reqd: 1
		// },
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
			
		},
		{
			fieldname: "from_datetime",
			label: __("From Datetime"),
			fieldtype: "Datetime",
			reqd: 1
		},
		{
			fieldname: "to_datetime",
			label: __("To Datetime"),
			fieldtype: "Datetime",
			reqd: 1
		}

	]
};

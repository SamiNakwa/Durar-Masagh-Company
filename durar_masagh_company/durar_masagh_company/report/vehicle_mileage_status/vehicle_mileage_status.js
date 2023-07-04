// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Mileage Status"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle"
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: "\nJan\nFeb"
		},
		{
			fieldname: "from",
			label: __("From"),
			fieldtype: "Date",
		},
		{
			fieldname: "to",
			label: __("To"),
			fieldtype: "Date",
		}
	]
};

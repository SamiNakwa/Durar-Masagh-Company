// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Current Status"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle"
		},
		{
			fieldname: "ignition",
			label: __("Ignition"),
			fieldtype: "Select",
			options: "\nAll\nYes\nNo",
			default: "All"
		},
	]
};

// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt
/* eslint-disable */


var month_dict = {
	1:'Jan',
	2:'Feb',
	3:'Mar',
	4:'Apr',
	5:'May',
	6:'Jun',
	7:'Jul',
	8:'Aug',
	9:'Sep',
	10:'Oct',
	11:'Nov',
	12:'Dec',
}

frappe.query_reports["Vehicle Mileage Status"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle",
			reqd: 1,
			default:'1201 UNB'
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: "\nJan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
			default: month_dict[frappe.datetime.str_to_obj(frappe.datetime.now_date()).getMonth() + 1]
			
		
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

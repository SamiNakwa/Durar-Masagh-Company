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
	],
	"formatter": function (value, row, column, data, default_formatter) {
		console.log(value, row, column)
		value = default_formatter(value, row, column, data);

		if (column.fieldname == 'type') {
			column.editable = true

			// value = `<select name="custom-type" id="custom-type">
			// 			<option value="Hold">Hold</option>
			// 			<option value="Bank">Bank</option>
			// 			<option value="opel">Bank-Workshop</option>
			// 			<option value="Cash">Cash</option>
			// 		</select>`
			// return value
		}

		if (column.fieldname == 'day') {
			if (value == 'Saturday') {
				value = `<b style="color:orange">${value}</b>`
				return value
			}
		}
		
		if (column.fieldname == 'attendance_status') {
			if (value == 'A') {
				value = `<b style="color:red">${value}</b>`
				return value
			} else if(value == 'P'){
				value = `<b style="color:green">${value} </b>`
				return value
			} else if (value == 'L') {
				value = `<b style="color:yellow">${value} </b>`
				return value
			} else if (value == 'H') {
				value = `<b style="color:blue">${value} </b>`
				return value
			}
		}
			
		return value

	}
};

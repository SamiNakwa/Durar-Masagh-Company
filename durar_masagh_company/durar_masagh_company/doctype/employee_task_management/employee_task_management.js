// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Task Management', {

	// refresh: function(frm) {

	// }

});



frappe.ui.form.on('Employee Task Details', { 
	start_datetime(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	},
	end_datetime(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	}

});


const calculate_time_duration = (frm, row) => {

	if (row.start_datetime && row.end_datetime){
		const durationInSeconds = calculateDurationInSeconds(row.start_datetime, row.end_datetime); 
		row.hours_spend = durationInSeconds

		frm.refresh_field('task_details')
	}
	
}


function calculateDurationInSeconds(startdatetime, enddatetime) {

	// Create two Date objects representing your datetime values
	const date1 = new Date(startdatetime);
	const date2 = new Date(enddatetime);

	// Calculate the difference in milliseconds
	const differenceInMilliseconds = date2 - date1;

	// Convert milliseconds to seconds
	const differenceInSeconds = differenceInMilliseconds / 1000;
  
	return differenceInSeconds;
  }
  





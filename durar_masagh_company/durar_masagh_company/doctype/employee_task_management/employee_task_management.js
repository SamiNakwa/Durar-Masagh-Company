// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Task Management', {

	refresh: function (frm) {
		if (frm.is_new()) {
			frm.trigger('get_current_employee')
		} else {
			frm.trigger('get_user_restriction')
		}
	},

	get_user_restriction(frm) {
		frm.call('get_current_employee')
			.then(r => {
				if (r.message) {
					let linked_doc = r.message;
					if (frm.doc.employee == linked_doc.employee) {
						frm.set_df_property('employee', 'read_only', 1)
						frm.set_df_property('employee_division', 'read_only', 1)
						frm.set_df_property('date', 'read_only', 1)
						frm.set_df_property('status', 'read_only', 1)
						frm.set_df_property('task_category', 'read_only', 1)
						frm.set_df_property('branch', 'read_only', 1)
						frm.set_df_property('assigned_by', 'read_only', 1)
						frm.set_df_property('additional_description', 'read_only', 1)
					}
				}
			})
		
	},
                                           
	get_current_employee(frm) {
		frm.call('get_current_employee')
			.then(r => {
				if (r.message) {
					let linked_doc = r.message;
					frm.doc.assigned_by = linked_doc.employee
					frm.refresh_field('assigned_by')
				} else {
				}
			})
	},

	// employee(frm) {
	// 	frm.trigger('check_is_employee_the_current_employee')
	// },

	check_is_employee_the_current_employee(frm) {
		frm.call('get_current_employee')
			.then(r => {
				if (r.message) {
					let linked_doc = r.message;
					if (frm.doc.employee == linked_doc.employee) {
						frm.set_value('employee', null)
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'orange',

							message: __("You can't assign yourself")
						});
					}
				} else {
				}
			})
	}

});



frappe.ui.form.on('Employee Task Details', { 
	start_datetime(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	},
	end_datetime(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	},
	form_render(frm, cdt, cdn) {

		frm.call('get_current_employee')
			.then(r => {
				if (r.message) {
					let linked_doc = r.message;
					if (frm.doc.employee == linked_doc.employee) {
						let row = locals[cdt][cdn]
						frm.set_df_property('task_details', 'read_only', 1, frm.docname, 'task_description', row.name)
						frm.set_df_property('task_details', 'read_only', 1, frm.docname, 'start_datetime', row.name)
						frm.set_df_property('task_details', 'read_only', 1, frm.docname, 'end_datetime', row.name)
						frm.set_df_property('task_details', 'read_only', 1, frm.docname, 'hours_spend', row.name)
						frm.refresh_field('task_details')
					}
				}
			})
		
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
  





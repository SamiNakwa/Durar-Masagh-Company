// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Maintenance Schedule', {
	before_save: function(frm) {
		const details = frm.doc.maintenance_details
		var count = 0
		if (details){
			for (let i = 0; i < details.length; i++){
				count += details[i].amount
			}
			frm.doc.total_amount = count
		}
	}
});


// Child Table
frappe.ui.form.on('Vehicle Maintenance Details', {
	amount(frm, cdt, cdn) {
		const details = frm.doc.maintenance_details
		var count = 0
		for (let i = 0; i < details.length; i++){
			count += details[i].amount
		}
		frm.doc.total_amount = count
		frm.refresh_field('total_amount')
	}

});
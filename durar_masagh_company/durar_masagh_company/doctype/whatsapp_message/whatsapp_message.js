// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whatsapp Message', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('WhatsApp Message Type', {
	
	field_name(frm, cdt, cdn){
		var child = locals[cdt][cdn]

		if (!(child.field_name.startsWith("wa_")) || str.includes(" ")){
			child.field_name = null
			frm.refresh_field('message_type')

			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __('The <b>Field Name</b> should starts with <b>wa_</b> and should not contain <b>Space</b> ')
			});
		}
	}
});
// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whatsapp Message', {
	refresh: function(frm) {
		console.log('refresh')
		frm.trigger('create_test_button')
	},
	create_test_button(frm){
		frm.add_custom_button(__("Test"), function() {
			let d = new frappe.ui.Dialog({
				title: 'Send Test Message',
				fields: [
					{
						label: 'Mobile Number',
						fieldname: 'mobile_number',
						fieldtype: 'Data',
						reqd: true
					},
					{
						label: 'Message',
						fieldname: 'message',
						fieldtype: 'Text',
						default: frm.doc.message
					},

				],
				size: 'large', // small, large, extra-large 
				primary_action_label: 'Sent',
				primary_action(values) {
					frappe.call({
						method: 'durar_masagh_company.durar_masagh_company.doctype.whatsapp_message.whatsapp_message.sent_test_whatsapp_message',
						args: {
							number: values.mobile_number,
							message: values.message
						},
						// disable the button until the request is completed
						btn: $('.primary-action'),
						// freeze the screen until the request is completed
						freeze: true,
						callback: (r) => {
							if (r.message){
								frappe.msgprint({
									title: __('Notification'),
									indicator: 'green',
									message: __('Test message send successfully')
								})
							}else{
								frappe.msgprint({
									title: __('Error'),
									indicator: 'red',
									message: __('Please check with Administrator or Dev-support')
								})
							}
						},
						error: (r) => {
							// on error
						}
					})

					d.hide();
				}
			});
			
			d.show();
		}).addClass('btn-primary');
	}
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
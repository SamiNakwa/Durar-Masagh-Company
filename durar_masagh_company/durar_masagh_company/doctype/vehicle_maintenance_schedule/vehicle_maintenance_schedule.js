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
	},
	before_workflow_action: function(frm){
		frm.call('vehicle_maintenance_notifcation');
	},
	is_tyre_changed: function(frm){
		frm.trigger('set_selected_tyre_filter');
	},
	set_selected_tyre_filter: function(frm){
		frm.call('get_vehicle_details')
		.then(r => {
			if (r.message) {
				let linked_doc = r.message;
				var tyre = linked_doc.tyre
				var service = linked_doc.service
				var service_list = tyre.concat(service)

				if (Boolean(frm.doc.is_tyre_changed)){
					frm.fields_dict['maintenance_details'].grid.get_field('product_or_service').get_query = function(doc, cdt, cdn) {
						var row = locals[cdt][cdn];
						return {
							filters: {
								name: ['in', service_list]
							}
						};
					};
					
					if(!(Boolean(tyre.length))){
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'green',
							message: __('Please configure tyre details in the Vehicle ' + frm.doc.vehicle)
						});
					}

				}else{
					frm.fields_dict['maintenance_details'].grid.get_field('product_or_service').get_query = function(doc, cdt, cdn) {
						var row = locals[cdt][cdn];
						return {
							filters: {
								name: ['in', service]
							}
						};
					};
				}
				
			}
		})

	}
});


// Child Table
frappe.ui.form.on('Vehicle Maintenance Details', {
	maintenance_details_add(frm, cdt, cdn) {
		if (!(Boolean(frm.doc.is_tyre_changed))){
			frm.set_query('product_or_service', 'maintenance_details', () => {
				return {
					filters: {
						is_tyre: 0
					}
				}
			})
		}
	},
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

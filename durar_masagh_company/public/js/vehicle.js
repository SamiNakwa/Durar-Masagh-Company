frappe.ui.form.on('Vehicle', {
	refresh: function(frm) {
        
        frm.trigger('update_arabitra_live_data')
        frm.trigger('set_query_in_product_service');
        frm.trigger('add_sync_location_custom_button');
	},
    update_arabitra_live_data: function(frm){
        frm.call('get_arabitra_data')
            .then(r => {
                if (r.message) {
                    let linked_doc = r.message;
                    console.log(linked_doc)
                    frm.doc.current_odometer = linked_doc.distance
                    frm.doc.ignition = linked_doc.ignition
                    frm.doc.current_location = linked_doc.location
                    // do something with linked_doc
                    frm.refresh_field('current_odometer')
                    frm.refresh_field('ignition')
                    frm.refresh_field('current_location')
                    frm.save()
                } else {
                    frappe.msgprint('There is no Arbitra logs for this vehicle please check with Arabitra')
                }
            })
    },
    set_query_in_product_service: function(frm){
        frm.fields_dict['tyre'].grid.get_field('tyre_position').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'is_tyre': 1  // Filter based on child field value
                }
            };
        };
    },
    add_sync_location_custom_button: function(frm){
        frm.add_custom_button(__("Sync Location"), function() {
            frm.call('sync_live_location')
                .then(r => {
                    frappe.msgprint(r.message)
                });
        }).addClass("btn-primary");

    }
});


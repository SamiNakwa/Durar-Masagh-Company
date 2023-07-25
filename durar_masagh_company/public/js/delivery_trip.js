frappe.ui.form.on("Delivery Trip", {
    refresh: function(frm){
        frm.trigger('set_deliverd_button')
        frm.trigger('set_driver_details')
    },
    set_deliverd_button: function(frm){
    
        if ((frm.doc.docstatus == 0) && (!Boolean(frm.doc.__islocal))){    
            if (frm.doc.delivery_status != 'Delivered'){
                frm.add_custom_button(__("Delivered"), function() {
                    if (frappe.user.has_role('Administrator') || frappe.user.has_role('Fleet Manager') || frappe.user.has_role('Driver')){
                        frappe.confirm('Are you sure you want to proceed? This process only for <b>Drivers</b>',
                            () => {

                                frm.remove_custom_button('Delivered');
                                frm.set_value('delivery_status', 'Delivered')
                                frm.call('set_delivery_status')
                                    .then(r => {
                                        if (r.message) {
                                            frappe.msgprint({
                                                title: __('Notification'),
                                                indicator: 'green',
                                                message: __('Delivery Status Updated Successfully')
                                            });
                                            frm.call('sent_delivery_status_update_message')
                                        }else{
                                            frappe.msgprint({
                                                title: __('Error'),
                                                indicator: 'red',
                                                message: __('Something wrong please check with Administrator')
                                            });

                                        }
                                        frm.refresh()
                                    })

                                // whatsapp message
                                // frm.call('sent_delivery_status_update_message')
                            }, () => {
                                // action to perform if No is selected
                            })
                    }
                }).css({"background-color": "green", "font-size": "15px", "color":"white"});
            }
            if (frm.doc.delivery_status == 'Not Delivered'){
                frm.add_custom_button(__("Partially Delivered"), function() {
                    if (frappe.user.has_role('Administrator') || frappe.user.has_role('Fleet Manager') || frappe.user.has_role('Driver')){
                        frappe.confirm('Are you sure you want to proceed? This process only for <b>Drivers</b>',
                            () => {

                                frm.remove_custom_button('Partially Delivered');
                                frm.set_value('delivery_status', 'Partially Delivered')
                                frm.call('set_delivery_status')
                                    .then(r => {
                                        if (r.message) {
                                            frappe.msgprint({
                                                title: __('Notification'),
                                                indicator: 'green',
                                                message: __('Delivery Status Updated Successfully')
                                            });
                                            frm.call('sent_delivery_status_update_message')
                                        }else{
                                            frappe.msgprint({
                                                title: __('Error'),
                                                indicator: 'red',
                                                message: __('Something wrong please check with Administrator')
                                            });

                                        }
                                        frm.refresh()
                                    })

                                // whatsapp message
                                // frm.call('sent_delivery_status_update_message')
                            }, () => {
                                // action to perform if No is selected
                            })
                    }
                }).css({"background-color": "orange", "font-size": "15px", "color":"white"});

            }
        }
    },
    set_driver_details(frm){

        if (Boolean(frm.doc.delivery_stops[0].delivery_note)){
            if (!Boolean(frm.doc.vehicle)){
                var delivery_note = frm.doc.delivery_stops[0].delivery_note
        
                var delivery_note_doc = frappe.get_doc('Delivery Note', delivery_note)

                frm.doc.vehicle = delivery_note_doc.vehicle
            }
            

        }

        // Driver Address check
        if (!(Boolean(frm.doc.driver_address))){
            if (Boolean(frm.doc.driver)){

                frm.call('get_driver_details')
                    .then(r => {
                        if (r.message) {
                            let linked_doc = r.message;
                            frm.doc.driver_address = linked_doc.address
                            frm.refresh_field('driver_address')

                        }
                    })
            }
            
        }
    }

});
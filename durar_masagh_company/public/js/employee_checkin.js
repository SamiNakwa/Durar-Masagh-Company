frappe.ui.form.on("Employee Checkin", {
    refresh(frm){
        user_restriction(frm);
        if(frm.is_new()){
            set_current_user_and_shift(frm);
            create_checkin_and_checkout_button(frm);
        }

        
    }

});


const create_checkin_and_checkout_button = (frm) => {
    if (frm.is_new()){
        frappe.call({
            method: "durar_masagh_company.durar_masagh_company.overrides.employee_checkin.get_last_employee_checkin",
            args: {doc:frm.doc},
            freeze: true,
            callback: function(r) {
                let linked_doc = r.message
                if(frm.doc.employee){
                    if(linked_doc.log_type){
                        if(linked_doc.log_type=='IN'){
                            var laple = '<i class="fa fa-sign-out" aria-hidden="true"></i> Check-Out'
                            var class_name = 'btn-danger'
                        }else if (linked_doc.log_type=='OUT'){
                            var laple = '<i class="fa fa-check"></i> Check-In'
                            var class_name = 'btn-primary'
                        }
                        frm.add_custom_button(laple, () => {
                            if(linked_doc.log_type=='IN'){
                                frm.set_value('log_type', 'OUT')
                            }else{
                                frm.set_value('log_type', 'IN')
                            }
                            set_current_location(frm)
                
                        }).addClass(class_name);

                    }else{
                        frm.add_custom_button('<i class="fa fa-check"></i> Check-In', () => {
                            frm.set_value('log_type', 'IN')
                            set_current_location(frm)
                        }).addClass('btn-primary');
                    }

                }
            }
        });

    }
}


const user_restriction = (frm) => {
    if (!(frappe.user.has_role('Developer'))){
        frm.disable_save();
        frm.set_df_property('employee', 'read_only', 1)
        frm.set_df_property('log_type', 'read_only', 1)
        frm.set_df_property('device_id', 'read_only', 1)
        frm.set_df_property('skip_auto_attendance', 'read_only', 1)
        frm.set_df_property('time', 'read_only', 1)
        frm.set_df_property('location', 'read_only', 1)

    }
}


const set_current_user_and_shift = (frm) => {
    frappe.call({
        method: "durar_masagh_company.durar_masagh_company.overrides.employee_checkin.get_current_user_data_and_shift",
        type: "POST",
        args: { user_id: frappe.session.user },
        async: false,
        callback: function(r) {
            let data = r.message
            if(data.employee){
                frm.set_value('employee', data.employee)
                if (data.shift_data) {
                    let shift_data = data.shift_data
                    frm.set_value('shift', shift_data.shift_type)
                    frm.set_value('shift_start', shift_data.shift_start)
                    frm.set_value('shift_end', shift_data.shift_end)
                    frm.set_value('shift_actual_start', shift_data.shift_actual_start)
                    frm.set_value('shift_actual_end', shift_data.shift_actual_end)
                }
            }else{
                frappe.msgprint({
                    title: __('Notification'),
                    indicator: 'orange',
                    message: __(`No employee marked for this current user <b>${frappe.session.user}</b>`)
                });
            }
        }
    });
    
}



const set_current_location = (frm) =>{
    navigator.geolocation.getCurrentPosition(function(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        let location_template = `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[${longitude},${latitude}]}}]}`
        // frm.set_value('location', location_template)
        frm.doc.location = location_template
        frm.refresh_field('location')
        frm.dirty()
        frm.save()
    })
}
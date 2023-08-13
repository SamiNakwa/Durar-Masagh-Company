frappe.ui.form.on("Employee Checkin", {
    refresh(frm){
        set_current_user(frm);
        create_checkin_and_checkout_button(frm);
        user_restriction(frm);
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
                console.log(linked_doc)
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
                        frm.save()
                    }).addClass(class_name);

                }else{
                    frm.add_custom_button('<i class="fa fa-check"></i> Check-In', () => {
                        frm.set_value('log_type', 'IN')
                        frm.save()
                    }).addClass('btn-primary');
                }
            }
        });

    }
}


const user_restriction = (frm) => {
    if (!(frappe.user.has_role('HR Manager'))){
        frm.disable_save();
        frm.set_df_property('employee', 'read_only', 1)
        frm.set_df_property('log_type', 'read_only', 1)
        frm.set_df_property('device_id', 'read_only', 1)
        frm.set_df_property('skip_auto_attendance', 'read_only', 1)

    }
}


const set_current_user = (frm) => {
    frappe.call({
        method: "durar_masagh_company.durar_masagh_company.overrides.employee_checkin.get_current_user_data",
        type: "POST",
        args: {user_id:frappe.session.user},
        callback: function(r) {
            let employee = r.message
            if(employee){
                frm.set_value('employee', employee)
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
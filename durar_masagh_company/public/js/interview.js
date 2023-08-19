frappe.ui.form.on('Interview', {

    before_save(frm){
        frm.call('get_applicant_name')
            .then(r => {
                if (r.message) {
                    let applicant_name = r.message;
                    frm.doc.costom_applicant_name = applicant_name
                    // frm.refresh_field('costom_applicant_name')
                }
            })
    }
});

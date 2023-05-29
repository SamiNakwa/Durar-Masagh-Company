frappe.ui.form.on('Vehicle', {
	refresh: function(frm) {
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
                }
            })
	},
});
// Copyright (c) 2023, Samiulla Nakwa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Field Staff Task Management', {
	 refresh(frm) {
		frm.trigger('create_custom_button')
	},
	create_custom_button(frm){
		frm.add_custom_button('Sync Location', function(){
			frm.trigger('update_geo_location')
		}).addClass('btn-primary')
	},
	update_geo_location(frm){
		navigator.geolocation.getCurrentPosition(function(position) {
			var latitude = position.coords.latitude;
			var longitude = position.coords.longitude;
			let location_template = `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[${longitude},${latitude}]}}]}`
			// frm.set_value('location', location_template)
			frm.doc.geo_location = location_template
			frm.refresh_field('location')
			frm.dirty()
			frm.save()
		})
	},
	status(frm){
		if (frm.doc.status == "Complete"){
			

		}
		alert('staus changes')

	}
});


const my_fun = () => {
	alert('my funtion')
}

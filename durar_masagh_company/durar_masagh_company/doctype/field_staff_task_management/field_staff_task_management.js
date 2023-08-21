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



frappe.ui.form.on('Meeting Details', { 
	start_time(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	},
	end_time(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		calculate_time_duration(frm, row)
	}

});


const calculate_time_duration = (frm, row) => {

	if (row.start_time && row.end_time){
		const durationInSeconds = calculateDurationInSeconds(row.start_time, row.end_time); 
		row.hours_spend = durationInSeconds

		frm.refresh_field('meeting_details')
	}
	
}


function timeToSeconds(time) {
	// Split the time into hours, minutes, and seconds
	const [hours, minutes, seconds] = time.split(':').map(Number);
  
	// Convert hours, minutes, and seconds to seconds
	const totalSeconds = (hours * 3600) + (minutes * 60) + seconds;
  
	return totalSeconds;
  }

function calculateDurationInSeconds(startTime, endTime) {
	const startSeconds = timeToSeconds(startTime);
	const endSeconds = timeToSeconds(endTime);
	const durationInSeconds = endSeconds - startSeconds;
  
	return durationInSeconds;
  }
  



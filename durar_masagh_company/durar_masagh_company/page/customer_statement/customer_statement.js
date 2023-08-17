frappe.pages['customer_statement'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Customer Statement Of Account',
		single_column: true
	});


	// Custom Button
    let $btn = page.set_primary_action('<i class="fa fa-file" aria-hidden="true"></i> Generate Report', () => create_generate_report())

	let btn = page.set_secondary_action('<i class="fa fa-print" aria-hidden="true"></i> Print', () => print_report())


	

/// Create Fields
let from_date_field = page.add_field({
	label: 'From Date',
	fieldtype: 'Date',
	fieldname: 'from_date',
	reqd: 1
});


let to_date_field = page.add_field({
	label: 'To Date',
	fieldtype: 'Date',
	fieldname: 'to_date',
	reqd: 1
});



let customer_field = page.add_field({
	label: 'Customer',
	fieldtype: 'Link',
	fieldname: 'customer',
	options: 'Customer',
	reqd: 1,
});

let statement_head_field = page.add_field({
	label: 'Statement Head',
	fieldtype: 'Data',
	fieldname: 'statement_head',
	reqd: 1,
});


// Primary Action Button
let$btn = page.set_primary_action('<i class="fa fa-file" aria-hidden="true"></i> Generate Report', () => generate_report()).addClass('btn-primary')

// Secondary Action - Print
let $print_btn = page.set_secondary_action('<i class="fa fa-print" aria-hidden="true"></i> Print', () => print_report()).addClass('btn-info')



const generate_report = () => {
	let values = get_form_values();
	let is_all_filled = check_all_fields_filled(values);

	if (is_all_filled){
		let form_data = get_form_data(values);

		// Before Render The page remove the existing page
		$('#print-format').remove()

		// render the template
		$(frappe.render_template("customer_statement", {data:form_data})).appendTo(page.body)

		frappe.msgprint({
			title: __('Notification'),
			indicator: 'green',
			message: __('Report Generated Successfully')
		});
	}
	
	
}


const get_form_values = () => {
	let values = {}
	for (const val in page.fields_dict){
		values[val] = page.fields_dict[val].value
	}
	return values
}

const check_all_fields_filled = (values) => {
	for(const key in values){
		if(!(values[key])){
			frappe.msgprint({
				title: __('Error'),
				indicator: 'red',
				message: __('Please Fill the all the fields')
			});
			return false
		}
	}
	return true
}


// Print Report
const print_report = () => {
	frappe.msgprint({
		title: __('Notification'),
		indicator: 'green',
		message: __('Printed Successfully')
	});
}


// Fetching all the data and form the report
const get_form_data = (values) => {

	let main_data = {}
	let no_of_days = get_no_of_days(values.from_date, values.to_date)
	let table_data = get_table_date(values)


	main_data['form_field'] = values
	main_data['no_of_days'] = no_of_days
	main_data['main'] = table_data

	return main_data
}

const get_no_of_days = (start_date, end_date) => {
	// Convert string dates to Date objects
	var start_date = new Date(start_date);
	var end_date = new Date(end_date);

	// Calculate the difference between the two dates in milliseconds
	var dateDifferenceMs = end_date - start_date;

	// Calculate the difference in days
	var dateDifferenceDays = dateDifferenceMs / (1000 * 60 * 60 * 24);

	if (dateDifferenceDays < 1){
		frappe.throw(`The <b>From Date</b> should be less than <b>To Date</b> `)
	}

	return dateDifferenceDays + ' Days'
}


const get_table_date = (values) => {
	var data
	frappe.call({
		method: "durar_masagh_company.durar_masagh_company.page.customer_statement.get_table_date",
		type: "POST",
		args: {filters:values},
		freeze: true,
		freeze_message: "Fetching Table Data",
		async: false,
		callback: function(r) {
			data = r.message
		}
	});

	return data

}

}

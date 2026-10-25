// Routes each user to one dashboard. Precedence: Driver > Salesperson > Employee.
// Page access and data are still checked again on each target page and in the APIs.
frappe.pages["my-dashboard"].on_page_load = function (wrapper) {
	const roles = frappe.user_roles || [];
	const has = (r) => roles.includes(r);
	let target = "employee-self-service";
	if (has("Driver Dashboard User")) target = "driver-dashboard";
	else if (has("Salesperson Dashboard User")) target = "salesperson-dashboard";
	frappe.set_route(target);
};

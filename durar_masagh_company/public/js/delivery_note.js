frappe.ui.form.on("Delivery Note", {

});

frappe.ui.form.on("Delivery Note Item", {

    delivery_quantity(frm, cdn, cdt){
        var child = locals[cdn][cdt]
        if (!(child.delivery_quantity > child.qty)){
            child.balance = child.qty - child.delivery_quantity
            frm.refresh_field('items')
        }else{
            frappe.throw('Delivery Quantity Is Should Not Be Greater Than Actual Quantity')
        }
    }
});
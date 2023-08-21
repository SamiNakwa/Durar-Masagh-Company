import frappe
from frappe.utils import getdate
import copy


@frappe.whitelist()
def get_table_date(filters):
    filters = frappe._dict(eval(filters))

    sales_invoice_list = frappe.db.get_all(
                            'Sales Invoice',
                            filters={
                                'customer': filters.customer,
                                'posting_date': ['between', [filters.from_date, filters.to_date]],
                                'docstatus':1,
                                'status':['!=', 'Paid']
                            },
                            fields=['*']
                        )

    if not sales_invoice_list:
        frappe.throw(f"There is no <b>Sales Invoice</b> data for this customer <b>{filters.customer}</b> in this dates {filters.from_date} to {filters.to_date}")

    sales_invoice_report = get_sales_invoice_report(sales_invoice_list)

    data = {'invoice_table': sales_invoice_report}
    return data



def get_sales_invoice_report(data):
    report = []
    payment_entry, pmr = get_payment_entry_date(data)

    for si in data:
        si = frappe._dict(si)
        paid_amount = get_paid_amount(si.name, payment_entry, pmr)
        template = {
            'transaction_date':si.posting_date,
            'refered_by':frappe.db.get_value('Sales Team', {'parent': si.name}, 'sales_person'),
            'invoice_no':si.name,
            'customer_reference':si.customer_reference,
            'invoice_amount': si.total,
            'paid_amount': paid_amount,
            'balance_amount': si.total - paid_amount,
            'net_overdue_days':None,
            'actual_due_date': si.due_date
        }

        report.append(template)
    
    return report




def get_payment_entry_date(data):

    name_list = [val.name for val in data]
    payment_entry_reference = frappe.db.get_all(
                                    'Payment Entry Reference',
                                    filters={
                                        'reference_name' : ['in', name_list ],
                                        'docstatus': 1
                                    },
                                    fields=['*']
                                )
    

    payment_entry = frappe.db.get_all(
                        'Payment Entry',
                        filters={
                                'name' : ['in', [pay.get('parent') for pay in payment_entry_reference] ],
                                'docstatus': 1
                            },
                        fields=['*']
                    )
    
    return payment_entry, payment_entry_reference



def get_paid_amount(sales_invoice, payment_entry, pmr):
    
    amount = 0

    for ref in pmr:
        if ref.get('refrence_name') == sales_invoice:
            for pe in payment_entry:
                if pe.name == ref.get('parent'):
                    amount += pe.get('total')
    
    return amount






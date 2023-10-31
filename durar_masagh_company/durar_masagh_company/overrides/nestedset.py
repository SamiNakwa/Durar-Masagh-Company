import frappe
from frappe import _
from frappe.query_builder.utils import DocType
from frappe.query_builder import Order
from frappe.utils.nestedset import rebuild_node


@frappe.whitelist()
def rebuild_tree(doctype, parent_field):
    """
    call rebuild_node for all root nodes
    """
    if parent_field == 'parent_employee':
        parent_field = 'reports_to'
    
    # if frappe.local.form_dict.parent_field == 'parent_employee':
    #     frappe.local.form_dict.parent_field = 'reports_to'

    # Check for perm if called from client-side
    if frappe.request and frappe.local.form_dict.cmd == "rebuild_tree":
        frappe.only_for("System Manager")

    meta = frappe.get_meta(doctype)
    if not meta.has_field("lft") or not meta.has_field("rgt"):
        frappe.throw(
            _("Rebuilding of tree is not supported for {}").format(frappe.bold(doctype)),
            title=_("Invalid Action"),
        )

    # get all roots
    right = 1
    table = DocType(doctype)
    column = getattr(table, parent_field)
    result = (
        frappe.qb.from_(table)
        .where((column == "") | (column.isnull()))
        .orderby(table.name, order=Order.asc)
        .select(table.name)
    ).run()

    frappe.db.auto_commit_on_many_writes = 1

    for r in result:
        right = rebuild_node(doctype, r[0], right, parent_field)

    frappe.db.auto_commit_on_many_writes = 0
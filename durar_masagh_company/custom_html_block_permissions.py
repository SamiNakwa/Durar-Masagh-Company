# Copyright (c) 2026, DM Group KSA
"""Record-level, deny-by-default access to Custom HTML Block for dashboard-only roles.

Users who can read Custom HTML Blocks through any existing role keep exactly the access
they have today. A user whose ONLY source of Custom HTML Block read access is a
dashboard role (e.g. "Driver Dashboard User") may read only the blocks listed for that
role. Every other block is denied, with or without User Permissions.

Wired in hooks.py through `has_permission` (single documents: form, API, workspace
rendering) and `permission_query_conditions` (lists, reports, link search).
"""

import frappe

DOCTYPE = "Custom HTML Block"

# dashboard role -> blocks that role alone may read
DASHBOARD_ROLE_BLOCKS = {
	"Driver Dashboard User": ("ESS UI - Driver",),
	"Employee Dashboard User": ("Employee Dashboard Prototype",),
}

ALWAYS_UNRESTRICTED = {"Administrator", "System Manager"}


def _roles_granting_read():
	"""Roles that grant READ on Custom HTML Block via role permissions, excluding the dashboard roles.

	Select-only roles are deliberately NOT counted: Select is not Read, so a user holding a
	Select-only role plus a dashboard role must stay restricted to the dashboard blocks."""
	roles = set()
	for p in frappe.get_meta(DOCTYPE).permissions:
		if (p.permlevel or 0) == 0 and p.read:
			roles.add(p.role)
	return roles - set(DASHBOARD_ROLE_BLOCKS)


def allowed_blocks(user=None):
	"""None = not restricted (normal permissions apply); otherwise the tuple of readable block names."""
	user = user or frappe.session.user
	if user == "Administrator":
		return None
	roles = set(frappe.get_roles(user))
	if roles & ALWAYS_UNRESTRICTED or roles & _roles_granting_read():
		return None
	dashboard_roles = roles & set(DASHBOARD_ROLE_BLOCKS)
	if not dashboard_roles:
		return None  # no read access at all; standard role checks already deny
	names = set()
	for r in dashboard_roles:
		names.update(DASHBOARD_ROLE_BLOCKS[r])
	return tuple(sorted(names))


def has_permission(doc, ptype=None, user=None):
	"""Frappe v14 `has_permission` hook. Only an explicit False is applied by Frappe
	(frappe.permissions.get_doc_permissions); None leaves the standard result unchanged,
	so this hook can only take access away, never grant it."""
	allowed = allowed_blocks(user)
	if allowed is None:
		return None  # no opinion: standard permissions decide
	if (ptype or "read") not in ("read", "select"):
		return False
	return None if doc.name in allowed else False


def get_permission_query_conditions(user=None, doctype=None):
	"""Frappe v14 `permission_query_conditions` hook, called as fn(user, doctype=...)."""
	allowed = allowed_blocks(user)
	if allowed is None:
		return ""
	names = ", ".join(frappe.db.escape(n) for n in allowed)
	return f"`tab{DOCTYPE}`.`name` in ({names})"

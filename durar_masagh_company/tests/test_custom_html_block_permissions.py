# Run: bench --site <site> run-tests --module durar_masagh_company.tests.test_custom_html_block_permissions
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from durar_masagh_company import custom_html_block_permissions as m

READ_ROLES = [
	"CEO", "IT Coordinator", "Metabase", "Internal Controller", "Purchase User", "Sales Person",
	"Technical Coordinator", "DMS Sales Person Access", "AR Accountant",
	"Manufacturing Dashboard Viewer", "Treasury Manager", "Driver Dashboard User",
	"Employee Dashboard User",
]
SELECT_ONLY_ROLES = ["Block Picker"]

USERS = {
	"driver@x": ["Employee", "Driver", "Driver Dashboard User", "All", "Guest"],
	"driver_select@x": ["Employee", "Driver Dashboard User", "Block Picker"],
	"driver_read@x": ["Employee", "Driver Dashboard User", "Sales Person"],
	"sales@x": ["Employee", "Sales Person"],
	"employee@x": ["Employee"],
	"selectonly@x": ["Employee", "Block Picker"],
	"empdash@x": ["Employee", "Employee Dashboard User"],
	"both@x": ["Employee", "Driver Dashboard User", "Employee Dashboard User"],
	"sysman@x": ["System Manager", "Driver Dashboard User"],
	"multi@x": ["CEO", "Driver Dashboard User"],
	"Administrator": ["Administrator"],
}


def meta(_dt):
	perms = [SimpleNamespace(role=r, read=1, select=0, permlevel=0) for r in READ_ROLES]
	perms += [SimpleNamespace(role=r, read=0, select=1, permlevel=0) for r in SELECT_ONLY_ROLES]
	return SimpleNamespace(permissions=perms)


def doc(name):
	return SimpleNamespace(name=name)


@patch.object(m.frappe, "get_meta", side_effect=meta)
@patch.object(m.frappe, "get_roles", side_effect=lambda u: USERS.get(u, []))
class TestCustomHTMLBlockPermissions(unittest.TestCase):
	def test_driver_allowed_block(self, *_):
		self.assertIsNone(m.has_permission(doc("ESS UI - Driver"), "read", "driver@x"))

	def test_driver_denied_other_blocks(self, *_):
		for name in ("CEO Command Center", "Employee Dashboard Prototype", "HR Dashboard Block"):
			self.assertIs(m.has_permission(doc(name), "read", "driver@x"), False)

	def test_driver_denied_write(self, *_):
		for ptype in ("write", "create", "delete", "export", "share"):
			self.assertIs(m.has_permission(doc("ESS UI - Driver"), ptype, "driver@x"), False)

	def test_driver_list_filter(self, *_):
		c = m.get_permission_query_conditions("driver@x", doctype="Custom HTML Block")
		self.assertIn("`tabCustom HTML Block`.`name` in (", c)
		self.assertIn("ESS UI - Driver", c)
		self.assertNotIn("CEO", c)

	# Driver Dashboard User + Select-only role must stay restricted (Select is not Read).
	def test_driver_with_select_only_role_stays_restricted(self, *_):
		self.assertIsNone(m.has_permission(doc("ESS UI - Driver"), "read", "driver_select@x"))
		self.assertIs(m.has_permission(doc("CEO Command Center"), "read", "driver_select@x"), False)
		self.assertIs(m.has_permission(doc("CEO Command Center"), "select", "driver_select@x"), False)
		self.assertIn("ESS UI - Driver", m.get_permission_query_conditions("driver_select@x"))

	# Driver Dashboard User + an existing Read role keeps that role's existing access (audited overlap).
	def test_driver_with_existing_read_role_unchanged(self, *_):
		self.assertIsNone(m.has_permission(doc("CEO Command Center"), "read", "driver_read@x"))
		self.assertEqual(m.get_permission_query_conditions("driver_read@x"), "")

	# Driver Dashboard User with no other block permission at all.
	def test_driver_without_other_block_permissions(self, *_):
		self.assertEqual(m.allowed_blocks("driver@x"), ("ESS UI - Driver",))

	# The restriction does not depend on User Permissions existing (deny-by-default).
	def test_driver_without_user_permission_still_restricted(self, *_):
		with patch.object(m.frappe, "get_all", create=True, return_value=[]) as get_all, \
			patch.object(m.frappe, "get_list", create=True, return_value=[]) as get_list:
			self.assertIs(m.has_permission(doc("CEO Command Center"), "read", "driver@x"), False)
			self.assertIn("ESS UI - Driver", m.get_permission_query_conditions("driver@x"))
			get_all.assert_not_called()
			get_list.assert_not_called()

	def test_select_only_user_without_dashboard_role_unaffected(self, *_):
		self.assertIsNone(m.has_permission(doc("CEO Command Center"), "select", "selectonly@x"))
		self.assertEqual(m.get_permission_query_conditions("selectonly@x"), "")

	# Employee Dashboard User may read only the Employee Dashboard block.
	def test_employee_dashboard_user_limited(self, *_):
		self.assertIsNone(m.has_permission(doc("Employee Dashboard Prototype"), "read", "empdash@x"))
		for name in ("CEO Command Center", "HR Dashboard Block", "Metabase Finance", "ESS UI - Driver"):
			self.assertIs(m.has_permission(doc(name), "read", "empdash@x"), False)
		self.assertIs(m.has_permission(doc("Employee Dashboard Prototype"), "write", "empdash@x"), False)
		c = m.get_permission_query_conditions("empdash@x")
		self.assertIn("Employee Dashboard Prototype", c)
		self.assertNotIn("ESS UI - Driver", c)

	# Holding both dashboard roles gives exactly the union of their two blocks.
	def test_both_dashboard_roles(self, *_):
		self.assertEqual(m.allowed_blocks("both@x"), ("ESS UI - Driver", "Employee Dashboard Prototype"))
		self.assertIsNone(m.has_permission(doc("ESS UI - Driver"), "read", "both@x"))
		self.assertIsNone(m.has_permission(doc("Employee Dashboard Prototype"), "read", "both@x"))
		self.assertIs(m.has_permission(doc("CEO Command Center"), "read", "both@x"), False)

	# No User Permission records are needed for the restriction.
	def test_employee_dashboard_user_without_user_permission(self, *_):
		with patch.object(m.frappe, "get_all", create=True, return_value=[]) as get_all:
			self.assertIs(m.has_permission(doc("CEO Command Center"), "read", "empdash@x"), False)
			get_all.assert_not_called()

	def test_unaffected_users(self, *_):
		for user in ("sales@x", "employee@x", "sysman@x", "multi@x", "Administrator"):
			self.assertIsNone(m.has_permission(doc("CEO Command Center"), "read", user))
			self.assertEqual(m.get_permission_query_conditions(user), "")

	def test_hook_never_grants(self, *_):
		for user in USERS:
			for name in ("ESS UI - Driver", "CEO Command Center"):
				for ptype in ("read", "select", "write"):
					self.assertIn(m.has_permission(doc(name), ptype, user), (None, False))

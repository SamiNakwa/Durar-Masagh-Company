from . import __version__ as app_version

app_name = "durar_masagh_company"
app_title = "Durar Masagh Company"
app_publisher = "Samiulla Nakwa"
app_description = "This is Custom app belongs to Durar Masagh Company"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@dmgroupksa.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/durar_masagh_company/css/durar_masagh_company.css"
# app_include_js = "/assets/durar_masagh_company/js/durar_masagh_company.js"

# include js, css files in header of web template
# web_include_css = "/assets/durar_masagh_company/css/durar_masagh_company.css"
# web_include_js = "/assets/durar_masagh_company/js/durar_masagh_company.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "durar_masagh_company/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
        "Vehicle" : "public/js/vehicle.js",
        "Delivery Note" : "public/js/delivery_note.js",
        "Delivery Trip" : "public/js/delivery_trip.js",
        "Employee Checkin" : "public/js/employee_checkin.js",
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "durar_masagh_company.install.before_install"
# after_install = "durar_masagh_company.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "durar_masagh_company.uninstall.before_uninstall"
# after_uninstall = "durar_masagh_company.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "durar_masagh_company.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Vehicle": "durar_masagh_company.durar_masagh_company.overrides.vehicle.CustomVehicle",
	"Delivery Note": "durar_masagh_company.durar_masagh_company.overrides.delivery_note.CustomDeliveryNote",
	"Delivery Trip": "durar_masagh_company.durar_masagh_company.overrides.delivery_trip.CustomDeliveryTrip",
	"Employee Checkin": "durar_masagh_company.durar_masagh_company.overrides.employee_checkin.CustomEmployeeCheckin"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"durar_masagh_company.schedule_job.vehicle_arabitra_logs.get_arabitra_data",
	],
	"daily": [
		"durar_masagh_company.schedule_job.vehicle.regulatory_compliance_checking",
		"durar_masagh_company.schedule_job.vehicle_arabitra_logs.update_vehicle_logs",
		"durar_masagh_company.schedule_job.driver.license_expairy_notification",
        "durar_masagh_company.schedule_job.vehicle_arabitra_logs.remove_unwanted_data"

	],
	# "hourly": [
	# 	"durar_masagh_company.tasks.hourly"
	# ],
	# "weekly": [
	# 	"durar_masagh_company.tasks.weekly"
	# ]
	# "monthly": [
	# 	"durar_masagh_company.tasks.monthly"
	# ]
    "cron": {
        "0 6 * * *": [
            "durar_masagh_company.schedule_job.whatsapp_message.send_good_morning_message"
        ]
    },
}

# Testing
# -------

# before_tests = "durar_masagh_company.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "durar_masagh_company.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "durar_masagh_company.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["durar_masagh_company.utils.before_request"]
# after_request = ["durar_masagh_company.utils.after_request"]

# Job Events
# ----------
# before_job = ["durar_masagh_company.utils.before_job"]
# after_job = ["durar_masagh_company.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"durar_masagh_company.auth.validate"
# ]


fixtures = [
    {"dt": "Workflow", "filters": [
        [
            "name", "in", [
                "Vehicle Maintenance Schedule",
            ]
        ]
    ]},
    {"dt": "Workspace", "filters": [
        [
            "name", "in", [
                "HR",
            ]
        ]
    ]},
    {"dt": "DocType Link", "filters": [
        [
            "parenttype", "in", [
                "Customize Form",
            ]
        ]
    ]},
    {"dt": "Custom Field", "filters": [
        [
            "dt", "in", [
                "Delivery Trip",
                "Vehicle",
                "Vehicle Log",
                "Location",
                "Delivery Note",
                "Delivery Note Item",
                "Asset Movement Item",
                "Appointment Letter",
                "Employee Checkin"
            ]
        ]
    ]},
    "Workflow State",
    "Workflow Action Master",
    "Email Template",
    "Role",
    "Whatsapp Message",
    "Custom DocPerm",
    "Custom Role",
    "Vehicle Service Type",
    "Role Profile",
    "Module Profile",
    "Appointment Letter Template"
    
]


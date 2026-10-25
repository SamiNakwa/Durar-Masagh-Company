# Files changed
- `employee_self_service/employee_self_service.js` — embeds exported Employee UI, replaces `ess_dashboard_assets` + `new Function` loader with static script.
- `salesperson_dashboard/salesperson_dashboard.js` — likewise Sales UI.
- `driver_dashboard/driver_dashboard.js` — likewise Driver UI.
- Corresponding `.css` files preserve full CSS sources for code review; styles are scoped in shadow DOM at runtime.
- Original `.json` role configurations and `my_dashboard` router files retained from deployment-ready ZIP.
- `DEPLOY.md` — updated checklist, security and rollback notes.
- No Server Script / ERPNext DB / permissions changes.

## Source lengths & SHA256 prefixes
- employee_self_service: script 70,878, CSS 33,200, resulting JS 105,472; source SHA256 prefix 5edc4c6b8c2c
- salesperson_dashboard: script 70,875, CSS 33,200, resulting JS 105,475; source SHA256 prefix b9ba4a4c4e24
- driver_dashboard: script 70,876, CSS 33,200, resulting JS 105,456; source SHA256 prefix d4d1acdf11a4

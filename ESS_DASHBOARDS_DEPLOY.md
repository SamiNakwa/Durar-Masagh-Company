# DM Group KSA — Four standalone role-based Desk Pages

## Source and integrity
The UI scripts and CSS are sourced from the `Custom HTML Block.csv` export, rows `ESS UI - Employee`, `ESS UI - Salesperson`, `ESS UI - Driver`. These scripts are included as **static Page JavaScript**. They are not retrieved using `ess_dashboard_assets` and are not passed through eval/new Function. Each Page renders its own shadow-root; the exported CSS is bundled as a static string injected into that ShadowRoot, and a separate CSS copy is provided for inspection. Never include that copy as a global Frappe stylesheet.

## Placement
Copy the `durar_masagh_company/durar_masagh_company/page/` folders into the matching path in your `durar_masagh_company` repo. Keep existing Page folders. Pages: `employee_self_service`, `salesperson_dashboard`, `driver_dashboard`, `my_dashboard`.

## Rollout order
1. Confirm app repository and deployed commit in Frappe Cloud.
2. Create roles `Driver Dashboard User` and `Salesperson Dashboard User` (Desk Access, no broad DocType rights) on **staging and production before site migrate**. Employee Page grants Employee or Employee Self Service. Assign new roles only to authorized employees after checking overlapping roles.
3. Review the exported UI code for privileged or accidental external requests and verify Page JSON roles. Verify live server APIs `ess_get_my_dashboard` and `ess_dashboard_assets` are role-checked; the new Pages need only `ess_get_my_dashboard`. Do not change these APIs or disable the old blocks yet.
4. Commit to a feature branch and deploy **staging first**, migrate/update the site and clear browser/bench cache.
5. Test with real authorized Driver, Light Driver, Salesperson, and ordinary Employee accounts: direct URLs and `/app/my-dashboard`, access denied for other variants, own trips/assets/vehicles/GPS only, vehicle-check writes, TAR September vs October historical behavior, docs and mobile.
6. After acceptance, deploy production; only then switch My Profile to `/app/my-dashboard`. Retain old workspace and backups during rollback window.

## Security
Each UI script still calls the existing server `ess_get_my_dashboard` with its own fixed `dashboard` key. The live server must enforce role + ownership for each call, regardless of Page access. Never grant general Custom HTML Block Read rights to Driver/Employee. The 76 old User Permissions may be removed only after accepted migration, with dependency review. Old block editor permissions still exist, but the new Pages no longer execute block code. `ess_dashboard_assets` can stay available only for the legacy system until safely retired.

## Limits
Syntax checked via Node.js. Not run in Frappe browser, not deployed, no real-login acceptance testing. Export contains all 3 actual UI blocks; each is intentionally a snapshot, meaning a future UI change requires a Git change and deployment.

## Rollback
Restore app branch/commit to version without these Pages and update site; point My Profile to the old page if previously switched. Server script backups `... Backup 20261025m` are unchanged by this bundle.

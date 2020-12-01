greeting = "Welcome to this Flask site!  <br>" \
           "<hr><h4>Default account credentials</h4>" \
           "user / password (User level 100, regular user) <br>" \
           "admin / password (User level 200, admin account) <br>" \
           "superadmin / password (User level 300, super admin account) <br>" \
            "<hr><h4>Authorization is controlled by custom decorators sprinkled throughout the code:</h4>" \
           "session_required<br>admin_required<br>super_admin_required<br><br>" \
           "Add Dog requires a login of any user level.<br>" \
           "View Dogs can be viewed by anyone, even if not logged in.<br>" \
           "- From within that page, you must be an Admin to Edit users or Super Admin " \
           "to delete dogs.<br>" \
           "View Users requires an Admin account.<br>" \
           "- From within that page, you must be a Super Admin to delete a user.<br>" \
           "Send Email requires an Admin account.<br>"

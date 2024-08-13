from django.contrib.admin.sites import AdminSite
from accounts.models import User


class BusinessAdminSite(AdminSite):
    site_title = 'Business CMS Admin'
    site_header = 'Business CMS'
    index_title = 'Business Administration'

    def has_permission(self, request):
        if request.user.is_authenticated:
            try:
                business = request.user.business
                return True
            except User.business.RelatedObjectDoesNotExist:
                return False
        return False
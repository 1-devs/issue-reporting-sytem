from rest_framework import permissions

class IsLeader(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False

        return request.user.role in ['DISTRICT_LEADER', 'SECTOR_LEADER', 'CELL_LEADER']
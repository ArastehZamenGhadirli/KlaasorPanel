from rest_framework.permissions import BasePermission

class HasGroupPermission(BasePermission):
    """
    This class for checking permissions for Groups 
    positive points: 
    reusable,
    works for all the groups,
    Accept single group or list of groups,
    Allow all access to superuser
    """
    def __init__(self, group_names):
        if isinstance(group_names, list):
            self.group_names = group_names 
        else:
            self.group_names = [group_names]
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True 
        return request.user.groups.filter(name__in=self.group_names).exists()




class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='MENTOR').exists()

class IsFinacialTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='FINANCIAL').exists()

class IsTeacherOrMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['MENTOR', 'TEACHER']).exists()

class IsRegisterSupport(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='REGISTER').exists()

class IsTicketSupport(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='TICKET').exists()

class IsNormal(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='NORMAL').exists()
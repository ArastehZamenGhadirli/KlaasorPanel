from rest_framework import permissions
from rest_framework.permissions import BasePermission



class IsMentor(permissions,BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name='MENTOR').exists()


class IsFinacialTeam(permissions,BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name='FINANCIAL').exists()





class IsTeacherOrMentor(permissions,BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name__in=['MENTOR','TEACHER']).exists()



class IsRegisterSupport(permissions,BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name='REGISTER').exists()

class IsTicketSupport(permissions,BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name='TICKET').exists()


    
    








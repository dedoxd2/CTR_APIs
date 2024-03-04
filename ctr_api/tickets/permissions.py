from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    
    # def has_permission(self, request, view):

    #     return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            #return bool(request.user == obj.user)    # mine
            return obj.author == request.user 
      #  return super().has_object_permission(request, view, obj)

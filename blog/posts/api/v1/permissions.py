from rest_framework.permissions import BasePermission



class IsPostOwner(BasePermission):
    message = "You aren't the owner of the post"

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        # Allow access only for post owners
       return  obj.author == request.user 

class IsPostCommentOwner(BasePermission):
    message = "You aren' the owner of the comment"

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # Allow access only for post comment owner
        return obj.user_that_comment == request.user
    

class IsReactionOwner(BasePermission):
    message = "You aren't the owner the reaction"

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        # Allow access only for reaction owner
        return obj.user_that_react == request.user


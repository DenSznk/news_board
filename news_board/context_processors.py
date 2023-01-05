from .models import Comment


def comments(request):
    user = request.user
    return {'comments': Comment.objects.filter(user=user)}

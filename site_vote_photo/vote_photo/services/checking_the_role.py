from django.http import Http404


def checking_the_role_user(user):
    if not (user.is_staff and user.is_superuser):
        raise Http404(
            f"{user.username} не является админом!" f" Зайдите на другой аккаунт."
        )

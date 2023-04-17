from django.shortcuts import render
from django.utils import timezone

from ..models import Notification


def notification_view(request):
    notification = Notification.objects.filter(recipient=request.user)
    notification_list_not_request_user = []
    for one_notification in notification:
        if one_notification.sender != request.user:
            one_notification.date_send_notification = (
                timezone.now() - one_notification.date_create
            )
            notification_list_not_request_user.append(one_notification)

    return render(
        request,
        "vote_photo/notification_view.html",
        {
            "title": "Уведомления",
            "notification": notification_list_not_request_user,
            "date_now": timezone.now(),
        },
    )


def get_current_unread_messages(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unreadCount = messageRequests.filter(is_read=False).count()

    else:
        unreadCount = 0

    return {
        'unreadCount': unreadCount
    }
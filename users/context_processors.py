"""
A global variable that can be accessed from all templates. I have to set it up in root directory settings.py under
templates
"""
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
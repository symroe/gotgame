from django.conf import settings

from sociallib.facebook.helpers import FacebookHelper


def get_facebook_helper(fb_token):
    return FacebookHelper(
        settings.GOTGAME_FACEBOOK_APP_ID,
        settings.GOTGAME_FACEBOOK_APP_SECRET,
        fb_token)

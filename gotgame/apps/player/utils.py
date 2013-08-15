from core.shortcuts import get_facebook_helper

from .models import Player


def create_or_update_player_from_token(fb_token):
    """
    Util function that creates or updates a Player given it's fb_token.

    It returns the tuple (player, created).
    It raises (:class: `facebook.GraphAPIError`) if the token is invalid.
    """
    helper = get_facebook_helper(fb_token)
    helper.validate_token()

    # creating or updating player
    fb_json = helper.get_me()
    fb_id = fb_json['id']

    player, created = Player.objects.get_or_create(fb_id=fb_id, defaults={
        'first_name': fb_json.get('first_name', ''),
        'last_name': fb_json.get('last_name', ''),
        'email': fb_json.get('email', '')
    })

    # always update fb data
    player.fb_token = fb_token
    player.fb_json = fb_json
    player.save()

    return player, created

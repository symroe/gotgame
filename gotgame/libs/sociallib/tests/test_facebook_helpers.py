import mock
import facebook
import datetime

from django.test import TestCase
from django.utils.timezone import utc

from sociallib.facebook.helpers import FacebookHelper
from sociallib.tests import data as social_test_data


class FacebookHelperTestCase(TestCase):
    def setUp(self):
        super(FacebookHelperTestCase, self).setUp()

        self.token = '1234566789'
        self.app_id = 'app-id'
        self.helper = FacebookHelper(self.app_id, 'app-secret', self.token)
        self.helper.graph = mock.MagicMock()

    def test_validate_token_invalid_token(self):
        # mocking get_object('app') => exception
        self.helper.graph.get_object.side_effect = facebook.GraphAPIError('Invalid token.')

        self.assertRaises(facebook.GraphAPIError, self.helper.validate_token)

    def test_validate_token_different_app_token(self):
        # mocking get_object('app') => dict
        self.helper.graph.get_object.return_value = {
                'id': 'wrong-app-id'
            }
        
        self.assertRaises(facebook.GraphAPIError, self.helper.validate_token)

    def test_validate_token_valid_token(self):
        # mocking get_object('app') => dict
        self.helper.graph.get_object.return_value = {
                'id': self.app_id
            }
        
        self.helper.validate_token()

    def test_get_me(self):
        # mocking get_object('app') => dict
        me_dict = {
            'bla': 1
        }
        self.helper.graph.get_object.return_value = me_dict
        
        self.assertEqual(self.helper.get_me(), me_dict)
    
    def test_fan_since(self):
        # is fan
        self.helper.graph.get_object.return_value = social_test_data.likes_get_object
        
        fan_since_datetime = datetime.datetime(
            year=2013, month=4, day=9, hour=9, minute=47, second=10
        ).replace(tzinfo=utc)
        self.assertEqual(self.helper.fan_since(12345), fan_since_datetime)

        # is not fan
        self.helper.graph.get_object.return_value = social_test_data.likes_get_object_no_result
        self.assertEqual(self.helper.fan_since(12345), None)
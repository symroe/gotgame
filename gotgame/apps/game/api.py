from django.conf.urls import url

from tastypie.resources import ModelResource
from tastypie import http
from tastypie.utils import trailing_slash

from .models import Profile, Banked


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
        allowed_methods = ['get']


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add-credits%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_credits'), name="add_credits"),
            url(r"^(?P<resource_name>%s)/bank%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('bank'), name="bank")
        ]

    def add_credits(self, request, **kwargs):
        """
            curl -v -X POST -H "Content-Type: application/json" --data '{"username": "myusername", "email": "player1@example.com", "credits": 5}' http://localhost:8000/api/v1/profile/add-credits/
        """
        self.method_check(request, allowed=['post'])

        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)

        # params
        params = {
            'username': deserialized.get('username'),
            'email': deserialized.get('email'),
            'credits': deserialized.get('credits')
        }

        for param in ['username', 'email', 'credits']:
            if not params[param]:
                return self.error_response(
                    request, '%s required' % param,
                    response_class=http.HttpBadRequest
                )

        profile, created = Profile.objects.get_or_create(
            username=params['username'],
            email=params['email']
        )

        profile.credits = params['credits']
        profile.save()

        return http.HttpNoContent()


    def bank(self, request, **kwargs):
        """
            curl -v -X POST -H "Content-Type: application/json" --data '{"username": "myusernamesss"}' http://localhost:8000/api/v1/profile/bank/

            Banks the credits of `username` only if credits > 0.
            Returns 404 if username not found, 204 otherwise.
        """
        self.method_check(request, allowed=['post'])

        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)

        # params
        username = deserialized.get('username')

        if not username:
            return self.error_response(request, 'username required', response_class=http.HttpBadRequest)

        # get profile
        try:
            profile = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return http.HttpNotFound()

        # bank it
        if profile.credits:
            Banked.objects.create(
                    profile=profile,
                    credits=profile.credits
                )

            # resetting profile.credits
            profile.credits = 0
            profile.save()

        return http.HttpNoContent()

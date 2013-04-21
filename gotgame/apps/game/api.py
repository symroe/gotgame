from django.conf.urls import url

from tastypie.resources import ModelResource
from tastypie import http
from tastypie.utils import trailing_slash

from .models import Profile


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
        allowed_methods = ['get']


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add-credits%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_credits'), name="add_credits")
        ]

    def add_credits(self, request, **kwargs):
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

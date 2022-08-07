from django.utils import translation


class AdminLocaleMiddleware(object):

    def process_request(self, request):
        if request.path.startswith('/admin'):
            translation.activate("en")
            request.LANGUAGE_CODE = translation.get_language()

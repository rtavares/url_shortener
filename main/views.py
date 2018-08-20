import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from url_shrtnr import utils
from url_shrtnr.models import UrlShortened
from url_shrtnr.settings import MAX_ORIG_URL_LENTGH

# Create your views here.


class UrlExpanderView(View):
    """
    - Get the shortened Url
    - Check if corresponds to a vlid Url already shortened
    - If yes, redirects to the original Url

    """

    def get(self, request, *args, **kwargs):
        url_shortened = kwargs.get('shortened')

        if url_shortened and len(url_shortened.strip() ) > 0:
            # Check if shortened url exists
            # If yes, redirect to site.
            # If not, display approprieted message

            url_shortned_obj = UrlShortened()

            url_orig = url_shortned_obj.check_existence_shortened(url_shortened)
            if url_orig:
                return redirect(url_orig)

            response = {
                'shortened_url_supplied':  url_shortened,
                'message':  "Does not exist",
            }
        else:
            response = {
                    "original_url": url_to_shorten,
                    "shortened": url_is_already_shortened,
                    "go_to_shortened": url_is_already_shortened,
                    "message": "already shortened",
                }

        return JsonResponse(response)

@method_decorator(csrf_exempt, name='dispatch')
class UrlShortenerView(View):
    """
    Main view for root page
    """
    responses = (
        "URL Ok.",
        "URL does not exist.",
        "URL is not a valid.",
    )

    response = {
        "API": "URL Shortener",
        "version": "1.0",
        "tnfo": "Usage of shortener API",
        "base": "/shorten_url/: this text ",
        "shortener_get": "shorten_url/<shortened_url>: via GET: redirects to original site if exists.",
        "shortener_post": "shorten_url/<url>: via POST: return the shortened url if valid or error message otherwise",
    }

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.response)

    def post(self, request, *args, **kwargs):
        received_json_data = json.loads(request.body.decode("utf-8"))
        url_to_shorten = received_json_data.get('url')

        if not url_to_shorten:
            return JsonResponse(self.response)

        if len(url_to_shorten) > MAX_ORIG_URL_LENTGH:
            response = {"error": "Url supplied is too long. Please supply an Url to shorter smaller than {}.".format(MAX_ORIG_URL_LENTGH)}
            return JsonResponse(response)

        # Maybe the requested url have already been shortened?
        url_shortned_obj = UrlShortened()

        url_is_already_shortened = url_shortned_obj.check_existence_original(url_to_shorten)
        if url_is_already_shortened:
            # Cool, just returen it! :-)
            response = {
                "original_url": url_to_shorten,
                "shortened": url_is_already_shortened,
                "go_to_shortened": "http://"+request.META['HTTP_HOST']+"/"+url_is_already_shortened,
                "message": "already shortened",
            }
            return JsonResponse(response)

        # Else... Let's keep working!
        shortener = utils.ShortenUrl(url_to_shorten)
        validurl_response = shortener.validate_url()

        if validurl_response == 0:
            """
            Supplied url is valid an exists. Let's shorten it
            """
            shortened_url = shortener.shorten_url()

            response = {
                "original_url": url_to_shorten,
                "message": self.responses[validurl_response],
                "go_to_shortened": "http://" + request.META['HTTP_HOST'] + "/" + shortened_url,
                "shortened_url": shortened_url,
                "status": "success shortening url",
            }
        else:
            response = {
                "message": self.responses[validurl_response],
                "url_to_shorten": url_to_shorten
            }

        return JsonResponse(response)

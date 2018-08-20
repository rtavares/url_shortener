"""
Utilitary classes
"""
import random
import requests
import string

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .settings import SHORTENED_URL_LENGTH

from url_shrtnr.models import UrlShortened

URL_ERROR = "URL parameter not supplied."

class ShortenUrl(object):
    """
    Receive a url, call for it's, validation, generate the shortened version,
    store it to DB and returns it.
    """
    def __init__(self, url_to_shorten):
        if not url_to_shorten or len(url_to_shorten) == 0:
            raise ValidationError(URL_ERROR)
        else:
            self.url_to_shorten = url_to_shorten

    def validate_url(self):
        """
        Verify validity of URL.
        :return:
        """
        # Verify validity of URL.
        url_validator = URLValidator()

        try:
            url_validator(self.url_to_shorten)
        except ValidationError:
            url_valid = False
        else:
            url_valid = True

        if url_valid:
            # Verify if URL exists

            try:
                request = requests.head(self.url_to_shorten)
            except Exception:
                response = 1  # Does not exists. Anything other than 200 is discarded
            else:
                if request.status_code == 200:
                    response = 0  # Url Ok
                else:
                    response = 1
        else:
            response = 2  # Not Valid - malformed

        return response

    def shorten_url(self):
        """
        After validation, perform the shortening to the supplied url

        Shortened url generation:
            Random picking SHORTENED_LENGTH characters from all lowercase, uppercase and digits.
            For SHORTENED_LENGTH = 6 and 62 letters and digits, it will give us 65^6 = 75 418 890 625 different
            possible combinations (combinatory with repetition).
            Once we are random choosing always from the same original universe, it allows repetitions of characters.

        :return: Shortened url
        """

        shortened_url = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(SHORTENED_URL_LENGTH))
        """ 
            Probability is low, but Murphy's law exists!
            So, let's check before if the generated shorter may already exist.
        """
        url_shortned_obj = UrlShortened()
        it_exists = url_shortned_obj.check_existence_shortened(shortened_url)

        if it_exists:
            # Ups! Duplication? How is it possible?
            # Lets go again...
            self.shorten_url()
        else:
            # We are good to go.
            # Save it.
            UrlShortened.objects.create(
                original_url=self.url_to_shorten,
                shortened_url=shortened_url
            )


        return shortened_url

    def save_shorten_url(self):
        """
        Save generated shortened url
        :return: True in case of success, False otherwise
        """
        pass

class ValidUrl(object):
    """
    Checks if url is valid before processing it.
    """
    def __init__(self, url_to_shorten):
        if not url_to_shorten or len(url_to_shorten) == 0:
            raise ValidationError(URL_ERROR)
        else:
            self.url_to_shorten = url_to_shorten

    def valid_url(self):
        url_validator = URLValidator()

        try:
            url_validator(self.url_to_shorten)
        except ValidationError:
            url_valid = False
        else:
            url_valid = True

        return url_valid


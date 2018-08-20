from django.db import models

from .settings import MAX_ORIG_URL_LENTGH

# Create your models here.

class UrlShortened(models.Model):
    """
    If MAX_ORIG_URL_LENTGH changes, we will have to run migrations to change the database table field.
    """
    shortened_url = models.CharField(max_length=10)
    original_url = models.CharField(max_length=MAX_ORIG_URL_LENTGH)

    def __str__(self):
        return self.shortened_url + " - " + self.original_url

    def check_existence_shortened(self, url_shortened):
        # We are expecting only one result, so we use 'get'.
        it_exists = False
        try:
            url_obj = UrlShortened.objects.get(shortened_url=url_shortened)
        except UrlShortened.DoesNotExist:
            # Nobody lives here...
            pass
        else:
            it_exists = url_obj.original_url
        return it_exists

    def check_existence_original(self, url_original):
        # We are expecting only one result, so we use 'get'.
        try:
            it_exists = UrlShortened.objects.get(original_url=url_original)
        except UrlShortened.DoesNotExist:
            # Not yet in the warehouse... Let's build it!
            it_exists = False
        else:
            # Ok, job done!
            # just return it!
            it_exists = it_exists.shortened_url

        return it_exists


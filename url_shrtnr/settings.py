"""
Setting the MAX_ORIG_URL_LENTGH value to an arbitrary value of 128.
(I like multiples of 8! ;-) )
    The RFC 2616 and RFC 7230 states that there is not theorethical limit for an Url length.
    Servers should be able to handle any kind of Url received, and rise an 414 (Request-URI Too Long)
    status response if are unable to process the too long Url.
    Even is recommended some kind 'agreed limit' of 2000, we here assumed that 128 should be more than enough to habdle
    our experimental shortner.
"""
MAX_ORIG_URL_LENTGH = 128
"""
    If MAX_ORIG_URL_LENTGH changes, we will have to run migrations on 'UrlShortened' Model 
    to change the database table field.
"""
SHORTENED_URL_LENGTH = 6

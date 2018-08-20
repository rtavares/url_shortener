URL Shortener - API

Test host: http://shortenurl.uk.to/shorten_url/

How to use:

        [HOST]/shorten_url/

        "API": "URL Shortener",
        "version": "1.0",
        "tnfo": "Usage of shortener API",
        "base": "/shorten_url/: this text ",
        "shortener_get": "shorten_url/<shortened_url>: via GET: redirects to original site if exists.",
        "shortener_post": "shorten_url/<url>: via POST: return the shortened url if valid or error message otherwise",

Example POST with curl:
    ```curl -H "Content-Type: application/json" --data '{"url":"http://www.google.com"}' http://shortenurl.uk.to/shorten_url/```

Example of shortened Url:
    ```http://shortenurl.uk.to/shorten_url/xtGIIL```
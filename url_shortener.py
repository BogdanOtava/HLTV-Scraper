import pyshorteners

def shorten_url(url:str):
    """
    Returns a shorter url for the url given as argument.

    Parameters:
        - url (str): the url that needs to be shorten.
    """


    shortener = pyshorteners.Shortener()

    return shortener.tinyurl.short(url)

"""
HTML Scrapers
"""
from debateservice.models import Opinion, Argument

def scrape_opinion_data(source: str) -> Opinion:
    """
    Scrape opinion data from a debate.org page source

    Parameters
    ----------
    source : str
        The opinion page source

    Returns
    -------
    Opinion
        The extracted opinion data
    """

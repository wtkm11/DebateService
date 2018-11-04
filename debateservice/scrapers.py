"""
HTML Scrapers
"""
from typing import Dict


def scrape_opinion_data(source: str) -> Dict:
    """
    Scrape opinion data from a debate.org page source

    Parameters
    ----------
    source : str
        The opinion page source

    Returns
    -------
    Dict
        The extracted opinion data
    """

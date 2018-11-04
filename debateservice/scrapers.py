"""
HTML Scrapers
"""
from bs4 import BeautifulSoup
from typing import Dict
from debateservice.exceptions import ParseException

def scrape_argument_data(source: str) -> Dict:
    """
    Scrape argument data from an HTML fragment

    Parameters
    ----------
    source : str
        The HTML fragment to scrape

    Returns
    -------
    Dict
        The extracted argument data
    """
    return {
        "author": source.find("cite").text.strip().replace("Posted by: ", ""),
        "description": source.find("p").text.strip()
    }

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

    Raises
    ------
    ParseException
        If an error occurred while parsing an opinion page
    """
    soup = BeautifulSoup(source, features="html.parser")

    try:
        name = soup.title.string.strip().replace(" | Debate.org","")
        yes_percent = soup.find("span", class_="yes-text").text.strip()
        no_percent = soup.find("span", class_="no-text").text.strip()
        arguments = soup.select(
            "div#yes-arguments li.hasData, div#no-arguments li.hasData"
        )
    except:
        raise ParseException()

    return {
        "name": name,
        "yes_percent": yes_percent,
        "no_percent": no_percent,
        "arguments": [scrape_argument_data(arg) for arg in arguments]
    }

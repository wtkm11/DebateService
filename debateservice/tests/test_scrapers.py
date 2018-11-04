"""
Tests of scrapers
"""

from unittest import TestCase
from debateservice.scrapers import scrape_opinion_data
from debateservice.exceptions import ParseException


class ScrapeOpinionDataTests(TestCase):
    """
    Tests of the scrape_opinion_data function
    """

    def test_scrape_opinions(self):
        """
        Test that an opinions page can be scraped
        """
        with open("./debateservice/tests/fixtures/opinion.html") as page:
            opinion_page = page.read()

        opinions = scrape_opinion_data(opinion_page)

        self.assertEqual(
            opinions,
            {
                "name": "Should drug users be put in prison?",
                "yes_percent": "50% Say Yes",
                "no_percent": "50% Say No",
                "arguments": [
                    {
                        "author": "Adalman",
                        "description": "Specifically speaking about hard drugs."
                    },
                    {
                        "author": "holla1755",
                        "description": "I don't like the argument."
                    },
                    {
                        'author': 'ihatethisname',
                        'description': 'Drug users were in tough times.'
                    }
                ]
            }
        )

    def test_scrape_empty(self):
        """
        Test that ParseException is raised if the opinion page cannot be parsed
        """
        with self.assertRaises(ParseException):
            opinions = scrape_opinion_data("<html></html>")

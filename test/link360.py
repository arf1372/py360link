# -*- coding: utf-8 -*-
import os
try:
    import json
except ImportError:
    import simplejson as json
import unittest
from pprint import pprint

from py360link.link360 import Link360Response, Bib

#Directory where test data is stored.  
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')

def read_data(filename):
    path = os.path.join(DATA_PATH, filename)
    content = open(path)
    return content

class TestArticleResponse(unittest.TestCase):

    def setUp(self):
        self.api_resp = read_data('article.xml')
        self.resp = Link360Response(self.api_resp)
        self.bib = Bib(self.resp.results()[0])

    def test_result_length(self):
        results = self.resp.results()
        self.assertEqual(len(results), 1)

    def test_query(self):
        query = self.resp.query()
        self.assertEqual(query, 
                        'version=1.0&url_ver=Z39.88-2004&id=pmid:19282400&sid=Entrez:PubMed')

    def test_library(self):
        lib = self.resp.library()
        self.assertEqaul(lib, 'Bob')

    def test_format(self):
        self.assertEqual(self.bib.format, 'journal')

    def test_btype(self):
        self.assertEqual(self.bib.btype(), 'article')

    def test_links(self):
        links = self.bib.get_links()
        for link in links:
            if link['type'] == 'article':
                self.assertEqual(link['anchor'], 'Full text available from SAGE Premier 2008.')
            elif link['type'] == 'journal':
                self.assertEqual(link['coverage_start'],  '2007-02-01')



class TestLinkSort(unittest.TestCase):

    def test_known_dbs(self):
        """
        [{'url': 'http://revproxy.brown.edu/login?url=http://online.sagepub.com/', 'coverage_start': '2007-02-01', 'type': 'source', 'anchor': 'SAGE Publications', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://jhs.sagepub.com/cgi/doi/10.1177/1753193408098482', 'coverage_start': '2007-02-01', 'type': 'article', 'anchor': 'Full text available from SAGE Premier 2008.', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://online.sagepub.com/1753-1934', 'coverage_start': '2007-02-01', 'type': 'journal', 'anchor': 'Journal website', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://jhs.sagepub.com/content/vol34/issue2/', 'coverage_start': '2007-02-01', 'type': 'issue', 'anchor': 'Browse this issue', 'provider': 'SAGE Publications'}]
        """
        pass


def suite():
    suite1 = unittest.makeSuite(TestArticleResponse, 'test')
    all_tests = unittest.TestSuite((suite1,))
    return all_tests

if __name__ == '__main__':
    unittest.main()

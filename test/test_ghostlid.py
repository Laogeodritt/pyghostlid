"""
PyGhostLid live tests against ghostbin.com

Project Name: PyGhostLid

"""
from unittest import TestCase
from time import sleep
import logging

from ghostlid import GhostLid

logging.basicConfig(level=logging.INFO)


class TestGhostBin(TestCase):
    """
    WARNING: This is a LIVE test. It will actually make queries against ghostbin.com. Alternative hosts are not tested.
    """

    _text = """
[04:10:07] <John> hi
[04:10:13] <Jane> hi
[04:19:21] <John> good talk
"""
    _lang = 'irc'
    _expire = '10m'

    def setUp(self):
        self.ghostlid = GhostLid(host='ghostbin.com', user_agent='PyGhostBinTest')
        self.ghostlid.load_languages()

        # Backwards compatibility with Py <3.2
        try:
            self.assertRegex
        except NameError:
            self.assertRegex = self.assertRegexpMatches

            def assertNotRegex(*args, **kwargs):
                return not self.assertRegex(*args, **kwargs)

            self.assertNotRegex = assertNotRegex

    def tearDown(self):
        sleep(1)  # prevent successive tests from making too many requests to the live service

    def test_load_languages(self):
        info = self.ghostlid.get_language_info()
        logging.info("\n=== Language Info Preview ===")
        logging.info(str(info)[0:1024])
        self.assertIsInstance(info, list, 'Language data structure: list')
        self.assertIsInstance(info[0], dict, 'Language data structure: list[dict]')
        self.assertIsInstance(info[0]['name'], str, 'Language data structure: list[{"name": str}]')
        self.assertIsInstance(info[0]['languages'], list, 'Language data structure: list[{"languages": list}]')
        self.assertIsInstance(info[0]['languages'][0]['id'], str,
                              'Language data structure: list[{"languages": [{"id": str}]}]')
        self.assertIsInstance(info[0]['languages'][0]['name'], str,
                              'Language data structure: list[{"languages": [{"name": str}]}]')

    def test_paste(self):
        paste_url = self.ghostlid.paste(self._text, lang=self._lang, expire=self._expire)
        self.assertRegex(paste_url, '^https://ghostbin\.com/paste/[A-Za-z0-9]+$', 'Returned paste URL')
        logging.info("\n=== Paste URL (for manual checking if desired) ===")
        logging.info(paste_url)

        # GhostBin main site has the /raw feature disabled - https://github.com/DHowett/ghostbin/issues/41
        # self.assertEqual(self._text, self.ghostlid.get_paste(self.ghostlid.get_paste_id(paste_url)),
        #                  "paste text matches")

    def test_get_lang_list(self):
        lang_list = self.ghostlid.get_lang_list()
        self.assertIn('python3', lang_list, 'check for ID python3 in list')
        self.assertIn('py3', lang_list, 'check for ID py3 (alt_id) in list')

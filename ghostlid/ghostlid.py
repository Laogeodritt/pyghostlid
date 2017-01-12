"""
Project Name: PyGhostLid

Submit and retrieve pastes from GhostBin within your application! This library supports both ghostbin.com and any
self-hosted instances of ghostbin.
"""

import urllib.request
import urllib.parse
import json

from ghostlid import __version__

_user_agent = 'PyGhostBin/{}'.format(__version__)


class NoRedirectErrorProcessor(urllib.request.HTTPErrorProcessor):

    def http_response(self, request, response):
        return response if 300 <= response.code < 400 \
            else urllib.request.HTTPErrorProcessor.http_response(self, request, response)

    https_response = http_response


class GhostLid:
    """
    Submit and retrieve pastes from Ghostbin within your application! This library supports both ghostbin.com and any
    self-hosted instances of ghostbin.

    Protocol information can be found here: https://ghostbin.com/paste/p3qcy
    """

    _url_opener = urllib.request.build_opener(NoRedirectErrorProcessor)

    def __init__(self, host='ghostbin.com', user_agent=_user_agent, defaults: dict=None):
        """
        Construct an instance to access a specific host, with a given user_agent and set of paste submission defaults.
        :param host: Optional. The hostname (and port, if needed) the Ghostbin instance is hosted on. By default the
            official 'ghostbin.com'.
        :param user_agent: Optional. The user-agent string to send. By default, 'PyGhostBin/' + version.
        :param defaults: A dict of default configurations for submitting a paste. See the named arguments for the
            ``paste()`` method (except `text`). Default defaults (lol) are 'lang': 'text', with no password or
            expiration.
        """
        self.host = host  # type: str
        self.user_agent = user_agent  # type: str
        self.defaults = {'password': None, 'expires': None, 'lang': 'text'}  # default defaults
        if defaults is not None:
            self.defaults.update(defaults)

        self.lang_info = None  # type: [dict]

    def load_languages(self) -> None:
        """
        Load the list of languages supported from the server. You should call this once after construction, or at
        any time the list must be updated from the server.

        You can retrieve the original structure with ``get_language_info()``, or a simple list of all accepted ``lang``
        values (see ``paste()``) with ``get_lang_list()``.
        :raise JSONDecodeError: Response from server was invalid and could not be decoded
        :raise KeyError: Response from server is missing expected language information
        """
        with urllib.request.urlopen(self.get_lang_url()) as r:
            self.lang_info = json.loads(r.read().decode('utf-8'))

    def paste(self, text: str, password: str=None, expire: str=None, lang: str=None) -> str:
        """
        Submit a paste to the Ghostbin website.

        :param text: Text of the paste.
        :param password: Encryption password. Do not pass or use None to use default. Empty string to explicitly use
            none.
        :param expire: How long until it expires. String, digits + "ns|us|ms|s|m|h\d". Maximum "15d".
        :param lang: Syntax colouring language, when retrieved on the website. The list of valid languages can be found
            programmatically from the``get_lang_list()`` list.
        :return: URL at which the paste can be accessed.
        :raise ValueError: parameter value is invalid. (If the value was not passed/left as default, the default
            passed in the constructor may be invalid.
        """
        args_struct = {
            'text': text,
            'password': password if password is not None else self.defaults['password'],
            'expire': expire if expire else self.defaults['expire'],
            'lang': lang if lang else self.defaults['lang']
        }

        if not args_struct['password']:
            del args_struct['password']

        # validate language
        if self.get_language_info() is None:
            self.load_languages()
        if args_struct['lang'] not in self.get_lang_list():
            raise ValueError('Invalid language', None, args_struct)

        # make request
        args_enc = urllib.parse.urlencode(args_struct).encode('utf-8')
        req = urllib.request.Request(self.get_paste_url(), data=args_enc, method='POST')
        req.add_header('User-Agent', self.user_agent)

        # process response
        with self._url_opener.open(req) as r:
            http_code = r.getcode()
            if http_code == 303:
                return 'https://' + self.host + r.getheader('Location')
            elif http_code == 400:
                raise ValueError('Bad request: ' + r.read().decode('utf-8'), 400, args_struct)
            else:
                raise ValueError('Unexpected response from server: ' + r.read().decode('utf-8'),
                                 http_code, args_struct)

    def get_paste(self, paste_id: str) -> str:
        """
        Retrieve the text of a paste.
        :param paste_id: The ID of a paste, i.e., in the URI /paste/{id}
        :return: The text of a paste. This is the plaintext paste - it does not contain any rendered formatting
            information.
        """
        with urllib.request.urlopen(self.get_retrieval_url_format().format(paste_id)) as r:
            return r.read().decode('utf-8')

    def get_paste_id(self, url):
        """
        From the URL, get paste ID.
        :param url: paste URL for this specific ghostbin instance
        :return: ID string
        :raise ValueError: not a valid URL for this ghostbin instance
        """
        import re
        try:
            return re.match('(https?://)?(www\.?)' + re.escape(self.host) + '/paste/([A-Za-z0-9]+)', url).group(1)
        except AttributeError as e:
            raise ValueError('Not a valid URL for this ghostbin instance') from e

    def get_language_info(self) -> [dict]:
        """
        Returns the structure defining supported languages. This structure has sufficient information to be usable for
        user display.

        This structure SHOULD NOT BE MODIFIED. Make a deep copy if you need it.

        ``get_lang_list()`` can be used to obtain a simple, flat list of all supported ``lang`` parameter values for the
        ``paste()`` function.
        :return: A structure describing all supported languages, broken down by category, of the form:

        .. code-block:: text
            languages.json := [...category...]
            category       := { "name": string, "languages": [...language...] }
            language       := { "id": string, "name": string, "alt_ids": [...string...] }

        May be ``None`` if ``load_languages()`` has not been called successfully yet.
        """
        return self.lang_info

    def get_lang_list(self) -> [str]:
        """
        Generate and return a list of all supported language IDs. This includes alternative IDs for the same language.
        :return: List of accepted ``lang`` ID strings for ``paste()``.
        """
        lang_list = []
        for category in self.get_language_info():
            for lang in category['languages']:
                lang_list.append(lang['id'])
                try:
                    lang_list.extend(alt_id for alt_id in lang['alt_ids'])
                except KeyError:
                    pass
        return lang_list

    def get_paste_url(self) -> str:
        return 'https://' + self.host + '/paste/new'

    def get_lang_url(self) -> str:
        return 'https://' + self.host + '/languages.json'

    def get_retrieval_url_format(self) -> str:
        return 'https://' + self.host + '/paste/{0}/raw'

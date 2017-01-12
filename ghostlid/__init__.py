"""
Project Name: PyGhostLid

Submit and retrieve pastes from GhostBin within your application! This library supports both ghostbin.com and any
self-hosted instances of ghostbin.
"""

__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Marc-Alexandre Chan <laogeodritt@arenthil.net>'
__maintainer__ = 'Marc-Alexandre Chan <laogeodritt@arenthil.net>'
__license__ = 'Modified BSD Licence <https://opensource.org/licenses/BSD-3-Clause>'
__copyright__ = 'Copyright (c) 2017 Marc-Alexandre Chan'

# must remain after metadata strings above
from ghostlid.ghostlid import GhostLid

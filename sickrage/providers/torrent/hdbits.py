# This file is part of SiCKRAGE.
#
# SiCKRAGE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SiCKRAGE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.


from urllib.parse import urlencode

import sickrage
from sickrage.core import MainDB
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.common import SearchFormats
from sickrage.core.exceptions import AuthException
from sickrage.core.helpers import try_int
from sickrage.core.tv.show.helpers import find_show
from sickrage.providers import TorrentProvider


class HDBitsProvider(TorrentProvider):
    def __init__(self):
        super(HDBitsProvider, self).__init__("HDBits", 'https://hdbits.org', True)

        self._urls.update({
            'search': '{base_url}/api/torrents'.format(**self._urls),
            'rss': '{base_url}/api/torrents'.format(**self._urls),
            'download': '{base_url}/download.php'.format(**self._urls)
        })

        self.username = None
        self.passkey = None

        self.cache = HDBitsCache(self, min_time=15)

    def _check_auth(self):
        if not self.username or not self.passkey:
            raise AuthException("Your authentication credentials for " + self.name + " are missing, check your config.")

        return True

    def _check_auth_from_data(self, parsed_json):
        if 'status' in parsed_json and 'message' in parsed_json:
            if parsed_json.get('status') == 5:
                sickrage.app.log.warning(
                    "Invalid username or password. Check your settings")

        return True

    def _get_season_search_strings(self, show_id, season, episode):
        post_data = {
            'username': self.username,
            'passkey': self.passkey,
            'category': [2],
            # TV Category
        }

        show_object = find_show(show_id)
        episode_object = show_object.get_episode(season, episode)

        if show_object.search_format in [SearchFormats.AIR_BY_DATE, SearchFormats.SPORTS]:
            post_data['tvdb'] = {
                'id': show_id,
                'season': str(episode_object.airdate)[:7],
            }
        elif show_object.search_format == SearchFormats.ANIME:
            post_data['tvdb'] = {
                'id': show_id,
                'season': "%d" % episode_object.scene_absolute_number,
            }
        else:
            post_data['tvdb'] = {
                'id': show_id,
                'season': episode_object.scene_season,
            }

        return [post_data]

    def _get_episode_search_strings(self, show_id, season, episode, add_string=''):
        post_data = {
            'username': self.username,
            'passkey': self.passkey,
            'category': [2],
            # TV Category
        }

        show_object = find_show(show_id)
        episode_object = show_object.get_episode(season, episode)

        if show_object.search_format == SearchFormats.AIR_BY_DATE:
            post_data['tvdb'] = {
                'id': show_id,
                'episode': str(episode_object.airdate).replace('-', '|')
            }
        elif show_object.search_format == SearchFormats.SPORTS:
            post_data['tvdb'] = {
                'id': show_id,
                'episode': episode_object.airdate.strftime('%b')
            }
        elif show_object.search_format == SearchFormats.ANIME:
            post_data['tvdb'] = {
                'id': show_id,
                'episode': "%i" % int(episode_object.scene_absolute_number)
            }
        else:
            post_data['tvdb'] = {
                'id': show_id,
                'season': episode_object.scene_season,
                'episode': episode_object.scene_episode
            }

        return [post_data]

    def _get_title_and_url(self, item):
        title = item['name']
        if title:
            title = self._clean_title_from_provider(title)

        url = self.urls['download'] + '?' + urlencode({'id': item['id'], 'passkey': self.passkey})

        return title, url

    def search(self, search_strings, age=0, show_id=None, season=None, episode=None, **kwargs):
        results = []

        sickrage.app.log.debug("Search string: %s" % search_strings)

        self._check_auth()

        resp = self.session.post(self.urls['search'], json=search_strings)
        if not resp or resp.content:
            sickrage.app.log.warning("Resulting JSON from provider isn't correct, not parsing it")
            return results

        try:
            parsed_json = resp.json()
        except ValueError:
            sickrage.app.log.warning("Resulting JSON from provider isn't correct, not parsing it")
            return results

        if self._check_auth_from_data(parsed_json):
            if not parsed_json or 'data' not in parsed_json:
                sickrage.app.log.warning("Resulting JSON from provider isn't correct, not parsing it")
                return results

            for item in parsed_json['data']:
                results.append(item)

        # sort by number of seeders
        results.sort(key=lambda k: try_int(k.get('seeders', 0)), reverse=True)

        return results


class HDBitsCache(TVCache):
    def _get_rss_data(self):
        results = []

        post_data = {
            'username': self.provider.username,
            'passkey': self.provider.passkey,
            'category': [2],
        }

        resp = self.provider.session.post(self.provider.urls['rss'], json=post_data)
        if not resp or not resp.content:
            return results

        try:
            parsed_json = resp.json()
        except ValueError:
            return results

        if self.provider._check_auth_from_data(parsed_json):
            results = parsed_json['data']

        return {'entries': results}

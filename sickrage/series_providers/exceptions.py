# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################


class SeriesProviderException(Exception):
    pass


class SeriesProviderError(SeriesProviderException):
    pass


class SeriesProviderNotAuthorized(SeriesProviderException):
    pass


class SeriesProviderAttributeNotFound(SeriesProviderException):
    pass


class SeriesProviderEpisodeNotFound(SeriesProviderException):
    pass


class SeriesProviderSeasonNotFound(SeriesProviderException):
    pass


class SeriesProviderShowNotFound(SeriesProviderException):
    pass


class SeriesProviderShowIncomplete(SeriesProviderException):
    pass

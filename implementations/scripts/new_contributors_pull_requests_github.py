# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CHAOSS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from datetime import datetime

from implementations.scripts.pullrequest_github import PullRequestGitHub
from implementations.scripts.utils import read_json_file


class NewContributorsPullRequestsGitHub(PullRequestGitHub):
    """
    Class for New Contributors Pull Requests in GitHub
    """

    def __init__(self, items, date_range=(None, None)):
        """
        Initializes self.items, the list with items (dictionary)
        as elements.

        :param items: A list of dictionaries.
            Each item is a Perceval dictionary, obtained from a JSON
            file or from Perceval directly.

        :param date_range: A tuple which represents the start and end date
            between which new contributors will be considered.
            Either, or both can be None. If, for example, since is None, that
            all unique contributors whose commit lies between the first pull request
            to the pull request which last falls inside the until range would be considered
            unique contributors.
        """
        super().__init__(items, date_range)

        self._filter_items()

        if self.since:
            self.items = [item for item in self.items if item['created_date'] >= self.since]

        if self.until:
            self.items = [item for item in self.items if item['created_date'] <= self.until]

    def _filter_items(self):
        new_contributors = {}

        for item in self.items:
            author = item['author']
            created_date = item['created_date']

            if author not in new_contributors or created_date < new_contributors[author]['created_date']:
                new_contributors[author] = item

        self.items = new_contributors.values()

    def compute(self):
        """
        Count the number of new contributors who has created an pull request
        between the two dates
        of date_range.

        :returns count_of_new_contributors: the number of new contributors who
            created a new pull request between the dates of date_range

            Since the dataframe self.df is modified in __init__ via groupby
            and idmin(), the number of unique entries in the dataframe gives us the number of the new contributors between the given dates.
        """
        return len(self.items)

    def __str__(self):
        return "New Contributors of Pull Requests"


if __name__ == '__main__':
    date_since = datetime.strptime("2018-01-01", "%Y-%m-%d")
    date_until = datetime.strptime("2018-07-01", "%Y-%m-%d")

    items = read_json_file('../pull_requests.json')

    # Total number of new contributors
    new_contributors = NewContributorsPullRequestsGitHub(items)
    print("New Contributors, total: {}".format(new_contributors.compute()))

    # restriting to a certain range
    new_contributors_dated = NewContributorsPullRequestsGitHub(items, (date_since, date_until))
    print("New Contributors, between 2018-01-01 and 2018-07-01: ", new_contributors_dated.compute())

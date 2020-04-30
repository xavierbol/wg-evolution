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

import unittest
import json
from datetime import datetime

from implementations.scripts.new_contributors_pull_requests_github import NewContributorsPullRequestsGitHub


def read_file(path):
    """
    Given a line-by-line JSON file, this function converts it to
    a Python dictionary and returns all such lines as a list.
    :param path: the path to the JSON file
    :returns items: a list of dictionaries read from the JSON file
    """
    with open(path, 'r') as raw_data:
        items = [json.loads(line) for line in raw_data]

    return items


class TestNewContributorsPullrequestsGitHub(unittest.TestCase):
    """
    Class to test the NewContributorsPullRequestsGithub class.
    """

    def setUp(self) -> None:
        """
        Run before each test to read the test data file
        """
        self.items = read_file('data/test_pulls_data.json')

    def test_compute(self):
        """
        Test the compute method of a NewContributorsPullRequestsGithub
        object with default parameters.
        """
        default_datetime = datetime.strptime("1970-01-01", "%Y-%m-%d")
        default_last_datetime = datetime.strptime("2100-01-01", "%Y-%m-%d")

        new_contributors = NewContributorsPullRequestsGitHub(self.items,
                                                             date_range=(default_datetime, default_last_datetime))

        authors = set()
        for item in self.items:
            authors.add(item['data']['user']['login'])

        count = new_contributors.compute()
        self.assertEqual(len(authors), count)


if __name__ == '__main__':
    unittest.main(verbosity=2)

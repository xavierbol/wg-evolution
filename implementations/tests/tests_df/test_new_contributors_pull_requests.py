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
#

import unittest
import json
from datetime import datetime

from pandas.testing import assert_frame_equal

from implementations.code_df.new_contributors_pull_requests_github import NewContributorsPullRequestsGitHub


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


class TestNewContributorsPullRequestsGitHub(unittest.TestCase):
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

    def test__agg(self):
        """
        Test the _agg method of a NewContributorsPullRequestsGithub
        object with default parameters when re-sampling
        on a weekly basis.
        """
        new_contributors = NewContributorsPullRequestsGitHub(self.items)
        new_contributors.df = new_contributors.df.set_index('created_date')
        test_df = new_contributors.df
        test_df = test_df.resample('W')['author'].agg(['count'])

        new_contributors.df = new_contributors._agg(new_contributors.df, 'W')
        assert_frame_equal(test_df, new_contributors.df)

    def test__get_params(self):
        """
        Test whether the _get_params method correctly returns
        the expected parameters for plotting a timeseries plot
        for the New Contributors Pull requests metric.
        """
        new_contributors = NewContributorsPullRequestsGitHub(self.items)
        params = new_contributors._get_params()

        expected_params = {
            'x': None,
            'y': 'count',
            'title': 'Trends in the Number of New Contributors',
            'use_index': True
        }

        self.assertEqual(expected_params, params)


if __name__ == '__main__':
    unittest.main(verbosity=2)

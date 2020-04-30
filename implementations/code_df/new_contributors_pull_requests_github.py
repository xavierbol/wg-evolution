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

from implementations.code_df.pullrequest_github import PullRequestGitHub
from implementations.code_df.utils import read_json_file


class NewContributorsPullRequestsGitHub(PullRequestGitHub):
    """
    Class for New Contributors Pull Requests in GitHub
    """

    def __init__(self, items, date_range=(None, None)):
        """
        Initializes self.df, the dataframe with one commit per row.

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

        self.df = self.df.loc[self.df.groupby('author')['created_date'].idxmin()]

        if self.since:
            self.df = self.df[self.df['created_date'] >= self.since]

        if self.until:
            self.df = self.df[self.df['created_date'] <= self.until]

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
        return len(self.df.index)

    def _agg(self, df, period):
        """
        Perform an aggregation operation on a DataFrame or Series
        to count the number of new contributors in a period when
        compared to contributors before that period.

        This method uses the 'count' aggregation method.

        :param df: a pandas DataFrame on which the aggregation will be
            applied.

        :param period: A string which can be any one of the pandas time
            series rules:
            'W': week
            'M': month
            'D': day

        :returns df: The final aggregated DataFrame
        """
        return df.resample(period)['author'].agg(['count'])

    def _get_params(self):
        """
        Return paramters for creating a timeseries plot

        :returns: A dictionary with axes to plot, a title
            and if use_index should be true when creating
            the plot.
        """
        title = "Trends in the Number of New Contributors"
        x = None
        y = 'count'
        use_index = True
        return {'x': x, 'y': y, 'title': title, 'use_index': use_index}

    def __str__(self):
        return "New Contributors of Pull Requests"


if __name__ == '__main__':
    date_since = datetime.strptime("2018-01-01", "%Y-%m-%d")
    date_until = datetime.strptime("2018-07-01", "%Y-%m-%d")

    items = read_json_file('../pull_requests.json')

    # Total number of new contributors
    new_contributors = NewContributorsPullRequestsGitHub(items)
    print("New Contributors, total: {}".format(new_contributors.compute()))

    print("Variations in the number of new contributors"
          " between 2018-01-01 and 2018-07-01: ")
    print(new_contributors.time_series(period='M'))

    # restriting to a certain range
    new_contributors_dated = NewContributorsPullRequestsGitHub(items, (date_since, date_until))
    print("New Contributors, between 2018-01-01 and 2018-07-01: ", new_contributors_dated.compute())

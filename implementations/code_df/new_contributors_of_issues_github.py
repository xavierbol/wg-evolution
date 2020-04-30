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

from implementations.code_df.issue_github import IssueGitHub
from implementations.code_df.utils import read_json_file


class NewContributorsOfIssuesGitHub(IssueGitHub):
    """
    Class for New Contributors of Issues in GitHub
    """

    def __init__(self, items, date_range=(None, None), reopen_as_new=False):
        """
        Initializes self.df, the DataFrame, with one issue per row.

        :param items: A list of dictionaries.
            Each item is a Perceval dictionary, obtained from a JSON
            file or from Perceval directly.

        :param date_range: A tuple which represents the period of interest
            It is of the form (since, until), where since and until are
            strings. Either, or both can be None. If, for example, since
            is None, that would mean that all issues from the first issue
            to the issue which last falls inside the until range will be
            included.

        :param reopen_as_new: A criteria for deciding whether reopened issues
            are considered as new issues. If True, every time an item is reopened,
            it is treated as a new issue.
        """
        self.all_contributors = set()
        for item in items:
            self.all_contributors.add(item['data']['user']['login'])
        super().__init__(items, date_range, reopen_as_new)

        self.df = self.df.loc[self.df.groupby('author')['created_date']
            .idxmin()]

        if self.since:
            self.df = self.df[self.df['created_date'] >= self.since]

        if self.until:
            self.df = self.df[self.df['created_date'] <= self.until]

    def compute(self):
        """
        Count the number of new contributors who has created an issue between the two dates
        of date_range.

        :returns count_of_new_contributors: the number of new contributors who
            created a new issue between the dates of date_range

            Since the dataframe self.df is modified in __init__ via groupby
            and idmin(), the number of unique entries in the dataframe gives
            us the number of the new contributors between the given dates.
        """
        return len(self.df.index)

    def _agg(self, df, period):
        """
        Perform an aggregation operation on a DataFrame or Series
        to count the number of new committers in a period when
        compared to committers before that period.

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
        Return parameters for creating a timeseries plot

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
        return "New Contributors of Issues"


if __name__ == '__main__':
    date_since = datetime.strptime("2018-01-01", "%Y-%m-%d")
    date_until = datetime.strptime("2018-07-01", "%Y-%m-%d")

    items = read_json_file('../pacman/issues.json')

    # Total number of new contributors
    new_contributors = NewContributorsOfIssuesGitHub(items)
    print("Total of new contributors: {}".format(new_contributors.compute()))

    print(new_contributors.df.author)

    print("Variations in the number of new contributors"
          " between 2018-01-01 and 2018-07-01: ")
    print(new_contributors.time_series(period='M'))

    # restricting to a certain range
    new_contributors_dated = NewContributorsOfIssuesGitHub(items, (date_since, None))
    print("New contributors, after 2018-03-08: ", new_contributors_dated.compute())

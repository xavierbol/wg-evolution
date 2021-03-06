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
# Authors:
#     Aniruddha Karajgi <akarajgi0@gmail.com>
#

from datetime import datetime

from implementations.code_df.pullrequest_github import PullRequestGitHub
from implementations.code_df.utils import (str_to_date,
                                           read_json_file)


class ReviewsDurationGitHub(PullRequestGitHub):
    """
    Class for Reviews Duration metric
    """

    def _flatten(self, item):
        """
        Flatten a raw pull_request fetched by Perceval into a flat dictionary.

        A list with a single flat directory will be returned.
        That dictionary will have the elements we need for computing metrics.
        The list may be empty, if for some reason the pull_request should not
        be considered.

        :param item: raw item fetched by Perceval (dictionary)
        :returns:   list of a single flat dictionary
        """

        creation_date = str_to_date(item['data']['created_at'])
        if self.since and (self.since > creation_date):
            return []

        if self.until and (self.until < creation_date):
            return []

        flat = {
            'repo': item['origin'],
            'hash': item['data']['id'],
            'category': "pull_request",
            'author': item['data']['user']['login'],
            'created_date': creation_date,
            'current_status': item['data']['state'],
            'merged': item['data']['merged']
        }
        if flat['merged'] is False:
            return []

        flat['duration'] = (str_to_date(item['data']['merged_at'])
                            - flat['created_date']).days

        return [flat]

    def compute(self):
        """
        Compute the median duration of reviews which were accepted, from the
        Perceval data.

        :returns median_review_duration: The median duration of a review.
        """

        median_review_duration = self.df['duration'].median()
        return median_review_duration

    def _agg(self, df, period):
        """
        Perform an aggregation operation on a DataFrame to median duration of
        reviews accepted in every interval of the period specified in the
        time_series method, like 'M', 'W',etc.

        It computes the median of the "duration" column of the
        DataFrame.

        :param df: a pandas DataFrame on which the aggregation will be
            applied.

        :param period: A string which can be any one of the pandas time
            series rules:
            'W': week
            'M': month
            'D': day

        :returns df: The aggregated dataframe, where aggregations have
            been performed on the "duration" column
        """

        df = df.resample(period)['duration'].agg(['median'])
        df = df.dropna()

        return df

    def _get_params(self):
        """
        Return parameters for creating a timeseries plot

        :returns: A dictionary with axes to plot, a title
            and if use_index should be true when creating
            the plot.
        """

        title = "Trends in the Duration of Reviews"
        x = None
        y = 'median'
        use_index = True
        return {'x': x, 'y': y, 'title': title, 'use_index': use_index}

    def __str__(self):
        return "Reviews Duration"


if __name__ == "__main__":
    date_since = datetime.strptime("2018-09-07", "%Y-%m-%d")
    items = read_json_file('../pull_requests.json')

    # median duration over all reviews
    reviews_duration = ReviewsDurationGitHub(items)
    print("The median reviews duration is {}"
          .format(reviews_duration.compute()))

    # median duration for reviews created after a certain date
    reviews_duration = ReviewsDurationGitHub(items, (date_since, None))
    print("The median reviews duration for reviews created after "
          "2018-09-07 which were accepted is {}"
          .format(reviews_duration.compute()))

    # time-series on a monthly basis for median duration of reviews
    print("The trends in the median duration for reviews created"
          " from 2018-09-07 onwards are: ")
    print(reviews_duration.time_series('M'))

from datetime import datetime

from implementations.code_df.issue_github import IssueGitHub
from implementations.code_df.utils import str_to_date, read_json_file


class IssueResolutionDurationGithub(IssueGitHub):
    """
    Class for the Issue Resolution Duration metric.
    """

    def _flatten(self, item):
        """
        Flatten a raw issue fetched by Perceval into a flat dictionary.

        A list with a single flat directory will be returned.
        That dictionary will have the elements we need for computing metrics.
        The list may be empty, if for some reason the issue should not
        be considered.

        :param item: raw item fetched by Perceval (dictionary)
        :returns:   list of a single flat dictionary
        """
        flat = super()._flatten(item)

        if flat:
            flat = flat[0]
        else:
            return flat

        if flat['current_status'] != 'closed':
            return []

        closed_date = str_to_date(item['data']['closed_at'])
        flat.update(
            closed_date=closed_date,
            resolution_duration=(closed_date - flat['created_date']).days)

        return [flat]

    def compute(self):
        """
        Compute the average of issue resolution duration for all issues in the Perceval data.

        :returns: the average of issue resolution duration
        """
        return self.df['resolution_duration'].mean()

    def compute_max(self):
        return self.df['resolution_duration'].max(skipna=True)

    def compute_min(self):
        return self.df['resolution_duration'].min(skipna=True)

    def _agg(self, df, period):
        """
        Perform an aggregation operation on a DataFrame to find
        the average age of issues created in a every
        interval of the period specified in the time_series method,
        like 'M', 'W',etc.

        It computes the mean of the 'open_issue_age' column of the
        DataFrame.

        :param df: a pandas DataFrame on which the aggregation will be
            applied.

        :param period: A string which can be any one of the pandas time
            series rules:
            'W': week
            'M': month
            'D': day

        :returns df: The aggregated dataframe, where aggregations have
            been performed on the "resolution_duration" column
        """
        df = df.resample(period)['resolution_duration'].agg(['mean'])
        df = df.dropna()

        return df

    def _get_params(self):
        """
        Return parameters for creating a timeseries plot

        :returns: A dictionary with axes to plot, a title
            and if use_index should be true when creating
            the plot.
        """
        title = "Trends in Issue Resolution Duration"
        x = None
        y = 'mean'
        use_index = True
        return {'x': x, 'y': y, 'title': title, 'use_index': use_index}

    def __str__(self):
        return "Issue Resolution Duration"


def display_result(issue_resolution_duration, title='all issues'):
    print('The average resolution duration of {} is {:.2f}'.format(title, issue_resolution_duration.compute()))
    print('The max resolution duration of {} is {:.2f}'.format(title, issue_resolution_duration.compute_max()))
    print('The min resolution duration of {} is {:.2f}'.format(title, issue_resolution_duration.compute_min()))


if __name__ == "__main__":
    date_since = datetime.strptime("2018-09-07", "%Y-%m-%d")
    items = read_json_file('../issues_events.json')

    issue_resolution_duration = IssueResolutionDurationGithub(items)
    display_result(issue_resolution_duration)

    # number of closed issues created after a certain date
    issue_resolution_duration = IssueResolutionDurationGithub(items, (date_since, None))
    display_result(issue_resolution_duration, 'issues created after 2018-09-07')

    # time-series on a monthly basis for the number of issues
    print("The changes in the resolution duration of issues on a monthly basis: ")
    print(issue_resolution_duration.time_series('M'))

from datetime import datetime

from implementations.scripts.issue_github import IssueGithub
from implementations.scripts.utils import read_json_file, str_to_date


class IssueResolutionDurationGithub(IssueGithub):
    """
    Issue Resolution Duration Metric
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
        Compute the average issue resolution duration for all issues in the Perceval data.

        :returns: the average resolution duration of issues
        """
        resolution_durations = [item['resolution_duration'] for item in self.items]
        return sum(resolution_durations) / len(resolution_durations)

    def compute_max(self):
        """
        Compute the maximum issue resolution duration for all issues in the Perceval data.

        :returns: the maximum resolution duration of issues
        """
        resolution_durations = [item['resolution_duration'] for item in self.items]
        return max(resolution_durations)

    def compute_min(self):
        """
        Compute the minimum open issue age for all issues in the Perceval data.

        :returns: the minimum resolution duration of issues
        """
        resolution_durations = [item['resolution_duration'] for item in self.items]
        return min(resolution_durations)

    def __str__(self):
        return "Issue Resolution Duration Metric for Github"


def display_result(issue_resolution_duration, title='all issues'):
    """
    Display the result of the average, maximum and minimum compute 
    for issue resolution duration metric.
    """
    print('The average resolution duration of {} is {:.2f} days.'.format(title, issue_resolution_duration.compute()))
    print('The max resolution duration of {} is {:.2f} days.'.format(title, issue_resolution_duration.compute_max()))
    print('The min resolution duration of {} is {:.2f} days.'.format(title, issue_resolution_duration.compute_min()))


if __name__ == "__main__":
    date_since = datetime.strptime("2018-09-07", "%Y-%m-%d")
    items = read_json_file('../issues.json')

    issue_resolution_duration = IssueResolutionDurationGithub(items)
    display_result(issue_resolution_duration)

    # number of closed issues created after a certain date
    issue_resolution_duration = IssueResolutionDurationGithub(items, (date_since, None))
    display_result(issue_resolution_duration, 'issues created after 2018-09-07')

from unittest import TestCase, main
import json
from pandas.util.testing import assert_frame_equal

from implementations.code_df.issue_resolution_duration_github import IssueResolutionDurationGithub


def read_file(path):
    """
    Given a line-by-line JSON file, this function converts it to
    a Python dictionary and returns all such lines as a list.

    :param path: the path to the JSON file

    :returns items: a list of dictionaries read from the JSON file
    """

    items = list()
    with open(path, 'r') as raw_data:
        for line in raw_data:
            line = json.loads(line)

            items.append(line)
    return items


class TestIssueResolutionDurationGithub(TestCase):
    def setUp(self):
        self.items = read_file('../data/test_issues_events_data.json')

    def test_compute(self):
        """
        Test the compute method of a IssueResolutionDurationGithub
        object instantiated with default parameters.
        """
        issues = IssueResolutionDurationGithub(self.items)
        expected_count = 48.4
        count = issues.compute()
        self.assertEqual(expected_count, count)

    def test_compute_reopen_as_new(self):
        """
        Test whether the reopen_as_new parameter works as expected
        """
        issues = IssueResolutionDurationGithub(self.items, reopen_as_new=True)
        expected_count = 46.23809523809524
        count = issues.compute()
        self.assertEqual(expected_count, count)

    def test_compute_max(self):
        """
        Test the compute_max method of a IssueResolutionDurationGithub object instantiated with the default parameters.
        """
        issues = IssueResolutionDurationGithub(self.items)
        expected_count = 167
        count = issues.compute_max()
        self.assertEqual(expected_count, count)

    def test_compute_min(self):
        """
        Test the compute_min method of a IssueResolutionDurationGithub object instantiated with the default parameters.
        """
        issues = IssueResolutionDurationGithub(self.items)
        expected_count = 0
        count = issues.compute_min()
        self.assertEqual(expected_count, count)

    def test__agg(self):
        """
        Test the _agg method of a IssueResolutionDuration
        object with default parameters when re-sampling
        on a weekly basis.
        """
        issues = IssueResolutionDurationGithub(self.items)
        issues.df = issues.df.set_index('created_date')
        test_df = issues.df.resample('W')['resolution_duration'].agg(['mean'])
        test_df = test_df.dropna()

        issues.df = issues._agg(issues.df, 'W')
        assert_frame_equal(test_df, issues.df)

    def test__get_params(self):
        """
        Test whether the _get_params method correctly returns
        the expected parameters for plotting a timeseries plot
        for the Issue Resolution Duration metric.
        """
        changes = IssueResolutionDurationGithub(self.items)
        params = changes._get_params()

        expected_params = {
            'x': None,
            'y': 'mean',
            'title': "Trends in Issue Resolution Duration",
            'use_index': True
        }

        self.assertEqual(expected_params, params)


if __name__ == "__main__":
    main(verbosity=2)

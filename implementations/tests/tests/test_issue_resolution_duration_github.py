from unittest import TestCase, main
import json

from implementations.scripts.issue_resolution_duration_github import IssueResolutionDurationGithub


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
        """
        Run before each test to read the test data file
        """
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

if __name__ == "__main__":
    main(verbosity=2)

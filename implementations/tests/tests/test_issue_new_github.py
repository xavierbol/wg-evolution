import unittest
import json

from implementations.scripts.issue_new_github import IssueNewGithub


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


class TestIssueNewGithub(unittest.TestCase):
    def setUp(self):
        """
        Run before each test to read the test data file
        """
        self.items = read_file('../data/test_issues_events_data.json')

    def test_compute(self):
        """
        Test the compute method of a IssueNewGithub
        object instantiated with default parameters.
        """
        issues = IssueNewGithub(self.items)
        expected_count = 20
        count = issues.compute()
        self.assertEqual(expected_count, count)

    def test_compute_reopen_as_new(self):
        """
        Test whether the reopen_as_new parameter works as expected.
        """
        issues = IssueNewGithub(self.items, reopen_as_new=True)
        expected_count = 21
        count = issues.compute()
        self.assertEqual(expected_count, count)


if __name__ == "__main__":
    unittest.main(verbosity=2)

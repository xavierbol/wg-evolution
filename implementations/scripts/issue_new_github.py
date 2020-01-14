from datetime import datetime

from implementations.scripts.issue_github import IssueGithub
from implementations.scripts.utils import read_json_file


class IssueNewGithub(IssueGithub):
    """
    Issues New
    """

    def compute(self):
        """
        Compute the number of new issues in the Perceval data.

        :returns: the number of issues created
        """
        return len(self.items)

    def __str__(self):
        return 'Issues New'


if __name__ == "__main__":
    date_since = datetime.strptime('2018-09-07', '%Y-%m-%d')
    items = read_json_file('../issues_events.json')

    # total new issues
    new_issues = IssueNewGithub(items)
    print("The total number of new issues is {:.2f}".format(new_issues.compute()))

    # new issues created after a certain date
    new_issues = IssueNewGithub(items, (date_since, None))
    print("The number of issues created after 2018-09-07 is {:.2f}".format(new_issues.compute()))

    # new issues created after a certain date and reopen issue is condering as new
    new_issues = IssueNewGithub(items, (date_since, None), reopen_as_new=True)
    print(
        "The number of issues created after 2018-09-07, considering reopened issues as new, is {:.2f}".format(new_issues.compute()))

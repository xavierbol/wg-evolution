from datetime import datetime

from implementations.scripts.issue_github import IssueGithub 
from implementations.scripts.utils import read_json_file

class IssueClosedGithub(IssueGithub):
    """
    Issues Closed metric
    """
    def compute(self):
        """
        Compute the number of closed issues in the Perceval data.

        :returns: the number of closed issues
        """
        closed_issues = [item['hash'] for item in self.items if item['current_status'] == 'closed']
        return len(closed_issues)

    def __str__(self):
        return 'Issues Closed'

if __name__ == "__main__":
    date_since = datetime.strptime('2018-09-07', '%Y-%m-%d')
    items = read_json_file('../issues_events.json')

    issues = IssueClosedGithub(items)
    print("The total number of closed issues is {:.2f}".format(issues.compute()))

    issues = IssueClosedGithub(items, (date_since, None))
    print('The number of issues closed after 2018-09-07, considering reopened issues as new, is {:.2f}'.format(issues.compute()))

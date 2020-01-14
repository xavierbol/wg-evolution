from datetime import datetime

from implementations.scripts.issue_github import IssueGithub
from implementations.scripts.utils import read_json_file


class IssueAgeGithub(IssueGithub):
    """
    Issue Age Metric
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

        if flat['current_status'] != 'open':
            return []

        flat['open_issue_age'] = (datetime.now() - flat['created_date']).days

        return [flat]

    def compute(self):
        """
        Compute the average open issue age for all issues in the Perceval data.

        :returns avg_open_issue_age: the average age of open
            issues
        """
        open_issue_ages = [item['open_issue_age'] for item in self.items]
        return sum(open_issue_ages) / len(open_issue_ages) if open_issue_ages else None

    def compute_max(self):
        """
        Compute the maximum open issue age for all issues in the Perceval data.

        :returns avg_open_issue_age: the average age of open
            issues
        """
        open_issue_ages = [item['open_issue_age'] for item in self.items]
        return max(open_issue_ages) if open_issue_ages else None

    def compute_min(self):
        """
        Compute the minimum open issue age for all issues in the Perceval data.

        :returns avg_open_issue_age: the average age of open
            issues
        """
        open_issue_ages = [item['open_issue_age'] for item in self.items]
        return min(open_issue_ages) if open_issue_ages else None

    def __str__(self):
        return "Issue Age Metric for Github"


if __name__ == "__main__":
    date_since = datetime.strptime("2018-09-07", "%Y-%m-%d")
    items = read_json_file('../issues.json')

    issue_age = IssueAgeGithub(items)
    print('The average age of all open issues is {:.2f}'.format(issue_age.compute()))
    print('The maximum age of a open issue is {:.2f}'.format(issue_age.compute_max()))
    print('The minimum age of a open issue is {:.2f}'.format(issue_age.compute_min()))

    # number of open issues created after a certain date
    issue_age = IssueAgeGithub(items, (date_since, None))
    print("The average age of open issues created after 2018-09-07 is {:.2f}".format(issue_age.compute()))

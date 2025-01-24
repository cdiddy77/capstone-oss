import os
from dotenv import load_dotenv

load_dotenv()
from github import Github
from github import Auth


auth = Auth.Token(os.getenv("GITHUB_TOKEN", ''))
g = Github(auth=auth)

# Specify the source and destination repositories
source_repo_name = "diamondkinetics/dk-product"
destination_repo_name = "diamondkinetics/sbot"


# Get the source and destination repositories
source_repo = g.get_repo(source_repo_name)
destination_repo = g.get_repo(destination_repo_name)

# Specify the issue number of the issue you want to move
issue_numbers_to_move = [
    1658,
    1659,
    1660,
    1661,
    1662,
    1663,
    1664,
    1665,
    1666,
    1668,
    1669,
    1670,
    1671,
    1672,
    1673,
    1674,
    1675,
    1676,
    1677,
    1678,
    1679,
    1680,
    1681,
    1682,
    1683,
    1684,
    1685,
    1686,
    1687,
    1688,
    1689,
    1690,
    1691,
    1692,
    1693,
    1694,
    1695,
    1696,
    1697,
    1698,
    1699,
    1700,
    1701,
    1702,
    1703,
    1704,
    1705,
    1706,
    1707,
    1708,
    1709,
    1710,
    1711,
    1712,
]

# Get the issue from the source repository
for issue_number_to_move in issue_numbers_to_move:
    print(f"Moving issue {issue_number_to_move}")
    issue_to_move = source_repo.get_issue(issue_number_to_move)

    # Create a new issue in the destination repository with the same title and body
    new_issue = destination_repo.create_issue(
        title=issue_to_move.title, body=issue_to_move.body
    )

    # Close the original issue in the source repository
    issue_to_move.edit(state="closed")

    # Add a comment to the original issue indicating it has been moved
    issue_to_move.create_comment(
        "This issue has been moved to {0}#{1}".format(
            destination_repo_name, new_issue.number
        )
    )

    print(
        "Issue successfully moved from {0} to {1}".format(
            source_repo_name, destination_repo_name
        )
    )

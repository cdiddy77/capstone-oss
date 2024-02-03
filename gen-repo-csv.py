from datetime import datetime, timedelta
from constants import target_labels
from github import Repository, Commit
from collections import defaultdict
from github import Github, Auth
import os
from dotenv import load_dotenv
load_dotenv()


auth = Auth.Token(os.getenv("GITHUB_TOKEN", ''))
g = Github(auth=auth)

# print(result.totalCount)

# keep a cache of information about each repo, so we dont re-fetch information
repoCache = defaultdict(dict)
# these are the keys of things we cache
REPO = 'repo'
LABELS = 'labels'
ISSUES = 'issues'
COMMIT_6MO = 'commit_6mo'


def clearRepoCache():
    repoCache.clear()

# given a repo and a field name, and a function to populate that field,
# ensure that the field is populated in the cache and return it
# the getter takes the repo as an argument


def ensureRepoCached(repo_name, field_name, getter):
    # if the repo isnt cached, cache it
    if repo_name not in repoCache:
        repoCache[repo_name][REPO] = g.get_repo(repo_name)
    # if the field in question isnt cached, cache it
    if field_name not in repoCache[repo_name]:
        repoCache[repo_name][field_name] = getter(
            repoCache[repo_name][REPO], repoCache[repo_name])
    # return the field
    return repoCache[repo_name][field_name]


def getRepoLabels(repo, cache):
    return [label.name for label in repo.get_labels()]


def getRepoIssues(repo: Repository.Repository, cache):
    return [issue for issue in repo.get_issues()]


six_months_ago = datetime.now() - timedelta(days=6*30)


def getRepoCommit6mo(repo: Repository.Repository, cache):
    commits = repo.get_commits(
        sha=repo.default_branch, since=six_months_ago)
    return [commit for commit in commits]


def getname(keydesc):
    if isinstance(keydesc, str):
        return keydesc
    elif isinstance(keydesc, tuple):
        return keydesc[0]
    else:
        raise Exception('Invalid keydesc type')


def getvalue(keydesc, repo):
    if isinstance(keydesc, str):
        return str(repo.raw_data[keydesc]).replace(',', ';')
    elif isinstance(keydesc, tuple):
        return str(keydesc[1](repo)).replace(',', ';')
    else:
        raise Exception('Invalid keydesc type')


def count_issues_with_target_labels(repo):
    common_target_labels = set(target_labels).intersection(
        set([l.name for l in repo.get_labels()]))
    issues = set()
    for tl in common_target_labels:
        for issue in repo.get_issues(state='open', labels=[tl]):
            issues.add(issue.id)
    return len(issues)


def count_unique_committers_6mo(repo: Repository.Repository):
    try:
        commits = ensureRepoCached(
            repo.full_name, COMMIT_6MO, getRepoCommit6mo)
        commit_users = set(
            [commit.author.login for commit in commits if commit.author and commit.author.login])
        return len(commit_users)
    except Exception as e:
        return -1


def top_five_committers_6mo(repo: Repository.Repository):
    try:
        commits: list[Commit.Commit] = ensureRepoCached(
            repo.full_name, COMMIT_6MO, getRepoCommit6mo)
        commit_users = set(
            [commit.author.login for commit in commits if commit.author and commit.author.login])
        return '|'.join(list(commit_users)[:5])
    except Exception as e:
        return '(exception: ' + str(e) + ')'


def top_ten_contributors(repo: Repository.Repository):
    try:
        contributors = repo.get_contributors()
        return '|'.join([c.login for c in contributors[:10]])
    except Exception as e:
        return '(exception: ' + str(e) + ')'


relevant_keys = [
    'id',
    'name',
    'full_name',
    ('owner', lambda repo: repo.raw_data['owner']['login']),
    'html_url',
    'description',
    'homepage',
    'size',
    'stargazers_count',
    'watchers_count',
    'language',
    'has_issues',
    'has_projects',
    'has_downloads',
    'has_wiki',
    'has_pages',
    'has_discussions',
    'forks_count',
    'archived',
    'disabled',
    ('license', lambda repo: repo.raw_data['license']
     ['name'] if repo.raw_data['license'] else '(none)'),
    'allow_forking',
    'is_template',
    'web_commit_signoff_required',
    ('topics', lambda repo: '|'.join(
        repo.raw_data['topics']) if repo.raw_data['topics'] else '(none)'),
    'forks',
    'open_issues',
    'created_at',
    'pushed_at',
    'watchers',
    'network_count',
    'subscribers_count',
    'default_branch',
    ('issues_with_target_labels', lambda repo: count_issues_with_target_labels(repo)),
    ('count_unique_committers_6mo', lambda repo: count_unique_committers_6mo(repo)),
    ('top_five_committers_6mo', lambda repo: top_five_committers_6mo(repo)),
    ('top_ten_contributors', lambda repo: top_ten_contributors(repo)),
    ('closed_issue_count_6mo', lambda repo: repo.get_issues(
        state='closed', since=six_months_ago).totalCount)
]

# filter certain languages
filter_out_languages = [
    'none'
]

result = g.search_repositories(
    query='stars:>10000', sort='forks', order='desc')


# print(','.join([getname(key) for key in relevant_keys]))
repo: Repository.Repository
for repo in result:
    clearRepoCache()  # each repo is independent, so clear the cache
    repoCache[repo.full_name][REPO] = repo
    if (repo.language or '').lower() in filter_out_languages:
        continue
    if repo.archived:
        continue

    values = []
    for key in relevant_keys:
        values.append(getvalue(key, repo))
    print(','.join(values), flush=True)

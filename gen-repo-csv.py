# %%
import os
from dotenv import load_dotenv
load_dotenv()
from github import Github
from github import Auth


auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
g = Github(auth=auth)


# %%
relevant_keys = [
'id',
'name',
'full_name',
('owner',lambda x: x['owner']['login']),
'html_url',
'description',
'fork',
'created_at',
'updated_at',
'pushed_at',
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
('license',lambda x: x['license']['name'] if x['license'] else '(none)'),
'allow_forking',
'is_template',
'web_commit_signoff_required',
('topics',lambda x: '|'.join(x['topics']) if x['topics'] else '(none)'),
'visibility',
'forks',
'open_issues',
'watchers',
'network_count',
'subscribers_count',
]

# %%
result = g.search_repositories(query='stars:>10000',sort='forks',order='desc')
# print(result.totalCount)

def getname(keydesc):
    if isinstance(keydesc, str):
        return keydesc
    elif isinstance(keydesc, tuple):
        return keydesc[0]
    else:
        raise Exception('Invalid keydesc type')
def getvalue(keydesc,value):
    if isinstance(keydesc, str):
        return str(value[keydesc])
    elif isinstance(keydesc, tuple):
        return str(keydesc[1](value))
    else:
        raise Exception('Invalid keydesc type')
    
print(','.join([getname(key) for key in relevant_keys]))
for repo in result[:3]:
    values = []
    for key in relevant_keys:
        values.append(getvalue(key,repo.raw_data))
    print(','.join(values))

# %%




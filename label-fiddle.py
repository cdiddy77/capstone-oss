import os
from dotenv import load_dotenv

load_dotenv()
from github import Github
from github import Auth


auth = Auth.Token(os.getenv("GITHUB_TOKEN", ''))
g = Github(auth=auth)

# Specify the source and destination repositories
repo_name = "your_repository_owner/your_repository_name"

# Get the repository
repo = g.get_repo(repo_name)

# Define the label name, color, and description
label_name = "bug"
label_description = "Issues related to bugs"

# Create the label
repo.create_label(label_name, label_color, label_description)

print(f"Label '{label_name}' created successfully in {repo_name}")
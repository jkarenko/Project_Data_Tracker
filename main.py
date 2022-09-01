import json
import os
from pathlib import Path
from jira import JIRA

conf_data = json.load(open("config.json", "r"))
SERVER = conf_data["jira_api"]
JIRA_URL = conf_data["jira_url"]
USER = conf_data["user"]
TOKEN = conf_data["token"]
PROJECT_INFO = conf_data["project_info"]


def connect_to_jira_with_token():
    print(f"Connect to {SERVER} with token")
    return JIRA(server=SERVER, token_auth=TOKEN)


def list_my_issues(jira, key=""):
    print(f"Get issues for {USER}")
    query = f"AND key = {key}" if key else ""
    issues = jira.search_issues(f"assignee = currentUser() AND status != Closed {query}", maxResults=100)
    issues_dict = {}
    for issue in issues:
        issues_dict[issue.key] = issue.fields.summary
    return issues_dict


def associate_cwd_with_jira_issue(issue_key, jira):
    print(f"Associate {issue_key} with {os.getcwd()}")


def associate_cwd_to_data(key, value="", is_issue=False):
    path = f"{str(Path.home())}/{PROJECT_INFO}"
    if not os.path.exists(path):  # create file if not exists
        with open(path, "w") as f:
            f.write('{"dirs": {}}')
    with open(path) as f:  # read file
        data = json.load(f)
        if os.getcwd() in data["dirs"]:  # dir already associated with issue
            if key in data["dirs"][os.getcwd()]:
                print(f"Already associated {os.getcwd()} with {key}")
                return
            if is_issue:
                if "issues" not in data["dirs"][os.getcwd()]:
                    data["dirs"][os.getcwd()]["issues"] = {}
                if key in data["dirs"][os.getcwd()]["issues"]:
                    print(f"Already associated {os.getcwd()} with {key}")
                    return
            if is_issue:
                print(f"Add {key} to {os.getcwd()}")
                data["dirs"][os.getcwd()]["issues"][key] = JIRA_URL + key
            else:
                print(f"Add {key} to {os.getcwd()}")
                data["dirs"][os.getcwd()][key] = value
        else:  # create new dir-data association
            print(f"Associate {os.getcwd()} with {key}")
            if is_issue:
                if os.getcwd() not in data["dirs"]:
                    data["dirs"][os.getcwd()] = {"issues": {key: JIRA_URL + key}}
                else:
                    data["dirs"][os.getcwd()]["issues"][key] = JIRA_URL + key
            else:
                data["dirs"][os.getcwd()] = {key: value}
        with open(path, "w") as ff:
            json.dump(data, ff, indent=4, sort_keys=True)


def open_config_file_in_default_editor():
    path = f"{str(Path.home())}/{PROJECT_INFO}"
    os.system(f"open -t {path}")


def main():
    # jira = connect_to_jira_with_token()
    # issues = list_my_issues(jira)
    associate_cwd_to_data("TEST-1", is_issue=True)
    associate_cwd_to_data("TEST-2", is_issue=True)
    associate_cwd_to_data(key="important link", value="https://www.google.com")
    open_config_file_in_default_editor()


if __name__ == "__main__":
    main()

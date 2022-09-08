import logging
import re
import sys
from git import GitCommandError

git_util_logger = logging.getLogger('auto_tag.git_util')

def create_tag(repo, tag, message=None):
    try:
        git_util_logger.info("Creating tag: %s", tag)
        tag = repo.create_tag(tag)
        repo.remotes.origin.push(tag.path, message=message)
    except GitCommandError as error:
        git_util_logger.error("\n %s", error) 

def get_remote_tags(repo, namespace):
    remote_tags = repo.git.ls_remote('--sort=-v:refname', '--tags', '.', f'{namespace}*')
    clean_tags = re.sub(r'([a-f0-9]{40}\trefs\/tags\/)+','', remote_tags).split('\n')
    return clean_tags

def check_tag(namespace, tag, repo):
    existing_tags = get_remote_tags(repo, namespace)
    if tag in existing_tags:
        return True
    return False

def filter_changed_files(repo, filter_file):
    current_commit = repo.head.commit
    diff_commit = repo.commit("main")
    if diff_commit == current_commit:
        diff_commit = repo.commit('HEAD~1')
    git_util_logger.info("Finding changed files between commits.")
    git_util_logger.info("Current Commit: %s.", current_commit)
    git_util_logger.info("Previous Commit: %s.", diff_commit)
    diff_files = current_commit.diff(diff_commit, create_patch=True)
    try:
        git_util_logger.info("Filtering the changed files.")
        filtered_files = [ file.a_path for file in diff_files if filter_file in file.a_path ]
        git_util_logger.debug("Filtered files: %s", filtered_files)
        return filtered_files
    except TypeError:
        git_util_logger.debug("There are no changed or modified files.")
        return []



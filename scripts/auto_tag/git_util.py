import logging
import re
import sys
from git import GitCommandError

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def create_tag(repo, tag, message=None):
    try:
        logging.info("Creating tag: %s", tag)
        tag = repo.create_tag(tag)
        repo.remotes.origin.push(tag.path, message=message)
    except GitCommandError as error:
        logging.error("\n %s", error) 

def get_remote_tags(repo, namespace):
    remote_tags = repo.git.ls_remote('--sort=-v:refname', '--tags', '.', f'{namespace}*')
    clean_tags = re.sub(r'([a-f0-9]{40}\trefs\/tags\/)+','', remote_tags).split('\n')
    return clean_tags

def check_tag(namespace, tag, repo):
    existing_tags = get_remote_tags(repo, namespace)
    if tag in existing_tags:
        logging.error('Tag: %s exists. Tag will not be created', tag)
        return True
    logging.debug('%s not found', tag)
    return False

def filter_changed_files(repo, filter_file):
    current_commit = repo.head.commit
    previous_commit = repo.commit('HEAD~1')
    logging.info("Finding changed files between commits.")
    logging.info("Current Commit: %s.", current_commit)
    logging.info("Previous Commit: %s.", previous_commit)
    diff_files = current_commit.diff(previous_commit, create_patch=True)
    try:
        logging.info("Filtering the changed files.")
        filtered_files = [ file.a_path for file in diff_files if filter_file in file.a_path ]
        logging.debug("Filtered files: %s", filtered_files)
        return filtered_files
    except TypeError:
        logging.debug("There are no changed or modified files.")
        return []



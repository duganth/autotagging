import yaml
from git import Repo
import os
from pathlib import Path 
import re
import logging
import sys

def get_namespace(path):
    namespace = re.match(r'modules\/[a-zA-Z0-9\/_-]+\/', path)
    if namespace:
        clean_namespace = re.sub(r'[^a-zA-Z0-9\/_-]', "_", namespace.group(0))
        return clean_namespace
    else:
        return None

def create_tag(repo, tag, message=None):
    try:
        logging.info(f"Creating tag: {tag}")
        tag = repo.create_tag(tag)
        repo.remotes.origin.push(tag.path, message=message)
    except:
        logging.error("failed") 

def get_version(file):
    try:
        with open(file, 'r') as f:
            tfmodule_content = yaml.safe_load(f)
    except yaml.YAMLError as exception:
       print(exception)
    return tfmodule_content['version']

def get_remote_tags(repo, namespace):
    remote_tags = repo.git.ls_remote('--sort=-v:refname', '--tags', '.', f'{namespace}*')
    clean_tags = re.sub(r'([a-f0-9]{40}\trefs\/tags\/)+','', remote_tags).split('\n')
    return clean_tags

def check_tag(namespace, tag, repo):
    existing_tags = get_remote_tags(repo, namespace)
    return tag in existing_tags

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
repo = Repo('.', search_parent_directories=True)
current_commit = repo.head.commit
commit_message = current_commit.message
logging.info(f"Current commit {current_commit}")
diff_files = current_commit.diff("HEAD~1", create_patch=True)

try:
    changed_files = [ a.a_path for a in diff_files if 'tfmodule.yaml' in a.a_path ]
except TypeError:
    changed_files = []

logging.info(f"Tagging {len(changed_files)} modules.")

for file in changed_files:
    version = get_version(file)
    namespace = get_namespace(file)
    tag = f'{namespace}{version}'
    if check_tag(namespace, tag, repo):
        logging.error(f"Tag exists skipping")
    else:
        create_tag(repo, tag)

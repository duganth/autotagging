import yaml
from git import Repo
import os
from pathlib import Path 
import re
import logging
import sys

def is_file(directory: Path, filename: str) -> bool:
    """Identifies if a file exists given a directory and filename"""
    file = directory / filename
    return file.exists()

def get_directories(files: list) -> list:
    """Helper function to return list of unique directories"""
    unique_directories = []
    directories = [Path(file).parent for file in files]
    [
        unique_directories.append(directory)
        for directory in directories
        if directory not in unique_directories
    ]
    return unique_directories

def get_module_directories(directories: list) -> list:
    """Identifies root module directories"""
    MODULE_DEFINITION_FILE = "tfmodule.yaml"
    module_directories = [
        directory
        for directory in directories
        if is_file(directory, MODULE_DEFINITION_FILE)
    ]
    return module_directories

def check_version_file(directories: Path, feature, main, staged_tf):
    for directory in directories:
        module_file = directory / 'tfmodule.yaml'
        current_version = yaml.safe_load(feature.tree[str(module_file)].data_stream.read())
        main_version = yaml.safe_load(main.tree[str(module_file)].data_stream.read())

def generate_tag(path):
    tag = re.match(r'modules\/[a-zA-Z0-9\/_-]+\/', path)
    if tag:
        clean_tag = re.sub(r'[^a-zA-Z0-9\/_-]', "_", tag.group(0))
        return clean_tag
    else:
        return None

def create_tag(repo, tag):
    try:
        logging.info(f"Creating tag: {tag}")
        tag = repo.create_tag(tag)
        repo.remotes.origin.push(tag.path)
    except:
        logging.error("failed") 

def get_tag(path):
    tag = re.search('modules', path)
    if tag:
        return tag.string
    return None

def get_version(file):
    try:
        with open(file, 'r') as f:
            tfmodule_content = yaml.safe_load(f)
    except yaml.YAMLError as exception:
       print(exception)
    return tfmodule_content['version']



logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
path = Path(os.path.dirname(os.path.abspath(__file__)))
repo = Repo(path, search_parent_directories=True)
current_commit = repo.head.commit
logging.info(f"Current commit {current_commit}")
diff_files = current_commit.diff("HEAD~1", create_patch=True)
try:
    changed_files = [ a.a_path for a in diff_files if 'tfmodule.yaml' in a.a_path ]
except TypeError:
    changed_files = []

logging.info(f"Tagging {len(changed_files)} modules.")

for file in changed_files:
    version = get_version(file)
    tag = generate_tag(file)
    create_tag(repo, f'{tag}{version}')

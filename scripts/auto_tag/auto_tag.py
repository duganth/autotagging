import yaml
from git import Repo
import os
from pathlib import Path 

def is_file(directory: Path, filename: str) -> bool:
    """Identifies if a file exists given a directory and filename"""
    file = directory / filename
    print(file)
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

def check_default_branch(repo):
    DEFAULT = "main"
    if repo.active_branch != DEFAULT:
        print("wrong")

path = Path(os.path.dirname(os.path.abspath(__file__)))
repo = Repo(path, search_parent_directories=True)
current_commit = repo.head.commit
main_commit = repo.commit("HEAD")
staged_tf = [ a.a_path for a in main_commit.diff("HEAD~1") if 'tfmodule.yaml' in a.a_path ]
bstaged_tf = [ a.b_path for a in main_commit.diff("HEAD~1") if 'tfmodule.yaml' in a.b_path ]
print(bstaged_tf)
check_default_branch(repo)
dirs = get_directories(staged_tf)
module_dirs = get_module_directories(dirs)
print(dirs)   
print(module_dirs)

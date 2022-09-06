from git import Repo
import os
from pathlib import Path

path = Path(os.path.dirname(os.path.abspath(__file__)))
repo = Repo(path, search_parent_directories=True)
current_commit = repo.head.commit
main_commit = repo.commit("HEAD")
staged_tf = [ a.a_path for a in repo.index.diff("HEAD~1") if 'tfmodule.yaml' in a.a_path ]
    
print(staged_tf)

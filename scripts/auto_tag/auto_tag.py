import logging
import sys
import terraffirm
import git_util
from git import Repo

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
repo = Repo('.', search_parent_directories=True)
changed_files = git_util.filter_changed_files(repo, 'tfmodule.yaml')
logging.info("Tagging %s modules.", len(changed_files))
for changed_file in changed_files:
    terraffirm_namespace = terraffirm.get_terraffirm_module_namespace(changed_file)
    version = terraffirm.get_terraffirm_module_version(changed_file)
    tag = f'{terraffirm_namespace}{version}'
    if not git_util.check_tag(terraffirm_namespace, tag, repo):
        git_util.create_tag(repo, tag)

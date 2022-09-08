import logging
import sys
import os
import terraffirm
import git_util
from git import Repo

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

logger = logging.getLogger('auto_tag')
logger.setLevel(LOGLEVEL)
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

def main():
    repo = Repo('.', search_parent_directories=True)
    changed_files = git_util.filter_changed_files(repo, 'tfmodule.yaml')
    logger.info("Tagging %s modules.", len(changed_files))
    for changed_file in changed_files:
        terraffirm_namespace = terraffirm.get_terraffirm_module_namespace(changed_file)
        version = terraffirm.get_terraffirm_module_version(changed_file)
        tag = f'{terraffirm_namespace}{version}'
        if not git_util.check_tag(terraffirm_namespace, tag, repo):
            git_util.create_tag(repo, tag)

if __name__ == '__main__':
    sys.exit(main())

import logging
import sys
import os
import terraffirm
import git_util
from git import Repo

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
DRYRUN = os.environ.get('DRYRUN', False)
DRY_RUN = not (os.getenv('DRY_RUN', 'True') == 'False')

logger = logging.getLogger('auto_tag')
logger.setLevel(LOGLEVEL)
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

def main():
    logger.info("DRY_RUN enabled: %s", DRY_RUN)
    repo = Repo('.', search_parent_directories=True)
    current_commit = repo.head.commit
    previous_commit = repo.commit("HEAD~1")
    changed_files = git_util.filter_changed_files(current_commit, previous_commit, repo, 'tfmodule.yaml')
    logger.info("Tagging %s modules.", len(changed_files))
    for changed_file in changed_files:
        terraffirm_namespace = terraffirm.get_terraffirm_module_namespace(changed_file)
        version = terraffirm.get_terraffirm_module_version(changed_file)
        tag = f'{terraffirm_namespace}{version}'
        try: 
            assert not git_util.check_tag(terraffirm_namespace, tag, repo)
            if DRY_RUN:
                logger.info(f"Planned tag: {tag}")
            else:
                git_util.create_tag(repo, tag)
        except AssertionError as e:
            logger.error('Tag: %s exists. Tag will not be created', tag)



if __name__ == '__main__':
    sys.exit(main())

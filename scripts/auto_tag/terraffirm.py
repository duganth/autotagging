import re
import yaml
import logging
import sys

terraffirm_logger = logging.getLogger('auto_tag.terraffirm')

def get_terraffirm_module_namespace(path):
    terraffirm_logger.debug("Path provided for namespace: %s", path)
    namespace = re.match(r'modules\/[a-zA-Z0-9\/_-]+\/', path)
    assert(namespace), "Namespace is not valid"
    terraffirm_logger.debug("Namespace: %s", namespace.group(0))
    clean_namespace = re.sub(r'[^a-zA-Z0-9\/_-]', "_", namespace.group(0))
    terraffirm_logger.debug("Clean Namespace: %s", clean_namespace)
    return clean_namespace

def get_terraffirm_module_version(version_file):
    try:
        with open(version_file, 'r', encoding="utf-8") as file:
            tfmodule_content = yaml.safe_load(file)
    except yaml.YAMLError as exception:
        print(exception)
    return tfmodule_content['version']

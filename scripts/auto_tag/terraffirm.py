import re
import yaml
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
def get_terraffirm_module_namespace(path):
    namespace = re.match(r'modules\/[a-zA-Z0-9\/_-]+\/', path)
    logging.debug("Namespace: %s", namespace)
    assert(namespace), "Namespace is not valid"
    clean_namespace = re.sub(r'[^a-zA-Z0-9\/_-]', "_", namespace.group(0))
    logging.debug("Clean Namespace: %s", clean_namespace)
    return clean_namespace

def get_terraffirm_module_version(version_file):
    try:
        with open(version_file, 'r', encoding="utf-8") as file:
            tfmodule_content = yaml.safe_load(file)
    except yaml.YAMLError as exception:
        print(exception)
    return tfmodule_content['version']

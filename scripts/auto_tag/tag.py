import re

def generate_tag(tag):
    clean_tag = re.sub(r'[^a-zA-Z0-9\/_-]', "_", tag)
    return clean_tag

def get_tag(path):
    tag = re.search(r'modules\/[a-zA-Z0-9\/_-]+/', path)
    #tag = re.search('modules', path)
    if tag:
        return tag.string
    else:
        return None
    

generate_tag("test-this-tag")
generate_tag("this?is2*ad.cige@test-this-tag")
print(get_tag("modules/help/"))
print(get_tag("les/help/"))

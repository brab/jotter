#######################
#
# Create slugs, derived from django's JS implementation
#
# name = "This IS A boOk's TiTle"
# slug = slugify(name)
#
# >>> print slug
# 'this-is-a-books-title'
#
#######################
import re

def slugify(inStr):
    removelist = ['a', 'an', 'as', 'at', 'before', 'but', 'by', 'for','from',
            'is', 'in', 'into', 'like', 'of', 'off', 'on', 'onto','per','since',
            'than', 'the', 'this', 'that', 'to', 'up', 'via','with'];
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b', '', inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug

def increment_slug(inStr):
    match = re.search('-[0-9]+$', inStr)
    if match:
        aslug = re.sub('[0-9]+$', str(int(inStr[match.start()+1:]) + 1), inStr)
    else:
        aslug = inStr + '-1'
    return aslug

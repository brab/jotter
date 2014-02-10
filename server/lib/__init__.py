import re


def increment_slug(slug):
    regex = r'^[-\w]+-(?P<number>\d+)$'
    match = re.search(regex, slug)
    if match:
        number = match.groupdict()['number']
        slug = slug[:-(len(number) + 1)]
        return '%s-%d' % (slug, int(number) + 1)
    else:
        return '%s-1' % slug

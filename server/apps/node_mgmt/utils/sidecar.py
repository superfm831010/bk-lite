from collections import defaultdict


def format_tags_dynamic(tags: list, allowed_prefixes: list):
    result = defaultdict(list)
    for tag in tags:
        if ":" in tag:
            key, value = tag.split(":", 1)
            if not value:
                continue
            if key in allowed_prefixes:
                value = value.split(",")
                result[key].extend(value)
    return dict(result)

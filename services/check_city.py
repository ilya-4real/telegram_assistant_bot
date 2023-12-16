import re 


def check_city_format(city: str):
    found = re.search(r'\D+', city)
    if found:
        return found.group()
    else:
        return None
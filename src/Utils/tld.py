from urllib.parse import urlparse

def get_tld(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')
    if len(domain_parts) >= 2:
        return domain_parts[-1]
    else:
        return None
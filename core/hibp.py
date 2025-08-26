import hashlib
import requests

HIBP_API_URL = "https://api.pwnedpasswords.com/range/"

def hash_password(password:str)->str :
    """Hash password with SHA-1 and return uppercase hex digest."""
    sha1= hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return sha1


def query_hibp_api(prefix :str)->str :
    """Query HIBP API with the hash prefix and return raw response text."""
    URL = HIBP_API_URL + prefix
    try:
        res = requests.get(URL ,timeout=5)
        res.raise_for_status()
        return res.text
    except requests.exceptions.RequestException as e :
        print(f"Error querying HIBP API: {e}")
        return ""


def is_pwned(password:str)-> tuple[bool,int]:
    """
    Check if the password has been leaked in a data breach.
    Returns (True, count) if found, else (False, 0).
    """
    sha1_hash = hash_password(password)
    prefix,suffix = sha1_hash[:5],sha1_hash[5:]
    hibp_response = query_hibp_api(prefix)
    if not hibp_response :
        return(False,0)
    for line in hibp_response.splitlines():
        hashsuffix,count = line.split(":")
        if hashsuffix == suffix :
            return(True, int (count))
    return (False,0)
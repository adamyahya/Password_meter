import re
import itertools
import string
import os

# =========================
# Configuration / Wordlists
# =========================
WORDLIST_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
WORDLIST_FILES = {
    "100k_most_used": "100k-most-used-passwords-NCSC.txt",
    "passwords": "passwords.txt",
    "names": "names.txt"
}

# L33t table for substitutions
LEET_TABLE = {
    '4': 'a', '@': 'a', '8': 'b', '(': 'c', '<': 'c', '{': 'c', '[': 'c',
    '3': 'e', '6': 'g', '9': 'g', '#': 'h', '!': 'i', '1': 'i', '|': 'i',
    '0': 'o', '$': 's', '5': 's', '7': 't', '+': 't', '2': 'z'
}
print(WORDLIST_DIR)

def load_wordlist(file : str)-> set :
    path = os.path.join(WORDLIST_DIR ,WORDLIST_FILES[file])
    with open (path ,"r", encoding="utf-8" )as f :
        return set(word.strip().lower() for word in f.readlines())


def match_dictionary(password : str , wordlist: set)->set :
    password_lower = password.lower()
    matches = []
    for word in wordlist:
        start = password_lower.find(word)
        if start != -1:
            matches.append({
                "pattern": "dictionary",
                "token": password[start:start+len(word)],
                "start": start,
                "end": start+len(word),
                "rank": 1  # can be enhanced with actual frequency rank
            })
    return matches

def generate_l33t_variants(token:str)-> list[str]:
    
    positions= [(i,c)for i,c in enumerate(token)if c in LEET_TABLE]
    if not positions:
        return [token]
    variants = set()
    for r in range(1,len(positions)+1):
        for comb in itertools.combinations(positions,r):
            lst = list(token)
            for pos, char in comb:
                lst[pos] = LEET_TABLE[char]
            variants.add("".join(lst))
    return list(variants)

def match_l33t (password: str,wordlist:set)-> list[dict]:
    matches= []
    password_lower = password.lower()
    variants = generate_l33t_variants(password_lower)
    for variant in variants:
        for word in wordlist :
            start = variant.find(word)
            if start != -1 :
                matches.append(
                    {
                    "pattern": "leet",
                    "token": password[start:start+len(word)],
                    "start": start,
                    "end": start+len(word),
                    "rank": 1   
                    }
                )
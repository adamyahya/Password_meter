import string

WEAK_WORDS = {"password", "123456", "qwerty", "iloveyou", "admin", "welcome"}

def check_length(password : str)-> bool :
    """Check if password meets NIST minimum length (8+)."""
    return len(password)>= 8


def check_character_variety(password:str)-> bool:
    """Check password contains at least 2 character categories."""
    categories = 0
    if any(c.islower() for c in password):
        categories += 1
    if any (c.isdigit() for c in password):
        categories +=1
    if any(c.isupper() for c in password):
        categories += 1
    if any(c in string.punctuation for c in password):
        categories += 1
    return categories >= 2

def check_common_patterns(password: str) -> bool:
    """Reject very simple/repetitive/sequential passwords."""
    
def check_dictionary_words(password: str, dictionary=WEAK_WORDS) -> bool:
    """Reject passwords that are common dictionary words."""
    return password.lower() not in dictionary



def policy_check(password : str)-> dict :
    results ={
       "length_ok": check_length(password),
        "common_pattern_ok": check_common_patterns(password),
        "variety_ok": check_character_variety(password),
        "dictionary_word_ok": check_dictionary_words(password),
   }
    results["final_decision"] = all(results.values())
    return results
print (policy_check("password"))

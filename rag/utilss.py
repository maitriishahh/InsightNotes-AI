import re
def extract_first_ts(chunk:str):
    match = re.search(r"\[(\d+):(\d+):(\d+)\]", chunk)
    if not match:
        return None
    
    h, m, s = map(int, match.groups())
    return h * 3600 + m * 60 + s
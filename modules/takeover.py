import json

def detect_takeover(subs):
    signs = json.load(open('data/takeover_signs.json'))
    for sub in subs:
        sub['takeover'] = False
        if sub.get('title') and any(sign.lower() in sub['title'].lower() for sign in signs):
            sub['takeover'] = True
    return subs

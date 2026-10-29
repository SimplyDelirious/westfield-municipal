"""Fictional town notices and sourced, curated 1984 historical events."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_events():
    return json.loads((ROOT / 'data' / 'events.json').read_text(encoding='utf-8'))

def fictional_event(category=None):
    events = load_events()['fictional']
    if category is not None and category not in events:
        raise ValueError('Unknown category')
    key = category or random.choice(list(events))
    return dict(random.choice(events[key]), category=key, kind='fictional')

def history_events(month=None, day=None):
    history = load_events()['history']
    if month is not None:
        history = [e for e in history if e['month'] == month]
    if day is not None:
        history = [e for e in history if e['day'] == day]
    return history

def choose_post(mode='mixed', month=None, day=None):
    if mode not in ('mixed', 'town', 'history'):
        raise ValueError('POST_MODE must be mixed, town, or history')
    candidates = history_events(month, day) if month and day else history_events()
    if mode == 'history':
        if not candidates:
            raise ValueError('No curated historical story for that date')
        return dict(random.choice(candidates), kind='history')
    if mode == 'mixed' and candidates and random.random() < .4:
        return dict(random.choice(candidates), kind='history')
    return fictional_event()

def embed_for(event):
    real = event['kind'] == 'history'
    desc = event['description']
    if real:
        desc += '\n\n**Historical source:** ' + event['source']
    else:
        desc += '\n\n*Roleplay hook: ' + event['hook'] + '*'
    fields = [{'name':'Type','value':'Real historical news — 1984' if real else 'Fictional town event','inline':True}]
    if real:
        fields.append({'name':'Historical date', 'value':f"{event['month']:02d}/{event['day']:02d}/1984",'inline':True})
    else:
        fields.append({'name':'Category', 'value':event['category'].title(),'inline':True})
    return {'title':event['title'], 'description':desc, 'color':0xA77C51,
            'author':{'name':'THE WESTFIELD GAZETTE'}, 'fields':fields,
            'footer':{'text':'1984 • '+('REAL HISTORY' if real else 'FICTIONAL ROLEPLAY')+' • No player outcomes imposed'}}

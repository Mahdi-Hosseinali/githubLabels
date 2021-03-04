import argparse
import json
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', help='github username that owns the repo')
parser.add_argument('-p', '--password', help='github password (if needed)')
parser.add_argument('-t', '--token', default=None, help='github token (if needed)')
parser.add_argument('-r', '--repo', help='github repo name')
parser.add_argument('-f', '--file', default='labels.json', help='output file name')
parser.add_argument('-a', '--action', default='get', help='`get` lables from repo to file or `set` repo lables from a file')
parser.add_argument('-e', '--endpoint', default='https://api.github.com', help='Endpoint server')
args = parser.parse_args()

endpoint = args.endpoint
URL = f'{endpoint}/repos/{args.user}/{args.repo}/labels'

# Setting the session
session = requests.Session()
if args.token is not None:
    session.headers['Authorization'] = 'token ' + args.token
elif args.user is not None and args.password is not None:
    session.auth = (args.user, args.password)
session.headers['Accept'] = 'application/vnd.github.v3+json'

# Get the lables first
r = session.get(URL)    
labels = json.loads(r.text)
print(f'Found {len(labels)} labels in the repo')

def filter_labels_for_post(labels):
    keep = ['name', 'color', 'description']
    return [{k:v for k, v in L.items() if k in keep} for L in labels]

if args.action.lower() == 'get':
    with open(args.file, 'w') as f:
        json.dump(labels, f)
    print('Saved all labels to ', args.file)
elif args.action.lower() == 'set':
    try:
        with open(args.file) as f:
            new_labels = json.load(f)
        new_labels = filter_labels_for_post(new_labels)
        print(f'Loaded {len(new_labels)} labels')
    except:     # noqa
        print('Could not read the label source file:', args.file)
        quit()

    if not new_labels:
        print('Not found any new labels')
        quit()

    # Remove all the current labels first
    print('Deleting current labels')
    for L in labels:
        r = session.delete(L['url'])
        if r.status_code == 204:
            print('Deleted label', L['name'])
        else:
            print(f'Could not delete', L['name'])
    
    # post the new labels
    for L in new_labels:
        r = session.post(URL, data=json.dumps(L))
        if r.status_code == 201:
            print('Added new label', L['name'])
        else:
            print('Failed to add label', L['name'])

import sys
import config
import requests
import os

headers = {'X-Api-Key': os.environ.get('API_KEY')}
data = requests.get(f'https://api.clockify.me/api/v1/workspaces/{os.environ.get("WORKSPACE_ID")}/projects',
                    headers=headers)

project = list(filter(lambda x: x['name'] == 'Daily CLI reporter', data.json()))
if not project:
    sys.exit()

proj_id = project[0]['id']
data = requests.get(
    f'https://api.clockify.me/api/v1/workspaces/{os.environ.get("WORKSPACE_ID")}/projects/{proj_id}/tasks',
    headers=headers)

tasks = [{'id': i['id'], 'name': i['name'], 'time': i['duration']} for i in data.json()]
for i in tasks:
    print(i['name'])

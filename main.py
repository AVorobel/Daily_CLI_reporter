import sys
import config
import requests
import os
import argparse
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Daily reporter')
parser.add_argument('project_name', metavar='name', type=str, nargs='+',
                    help='name of project')

args = parser.parse_args()

headers = {'X-Api-Key': os.environ.get('API_KEY')}
project_name = args.project_name[0]

data = requests.get(f'https://api.clockify.me/api/v1/workspaces/{os.environ.get("WORKSPACE_ID")}/projects',
                    headers=headers)

project = list(filter(lambda x: x['name'] == project_name, data.json()))
if not project:
    print('project not found')
    sys.exit()

proj_id = project[0]['id']
data = requests.get(
    f'https://api.clockify.me/api/v1/workspaces/{os.environ.get("WORKSPACE_ID")}/projects/{proj_id}/tasks',
    headers=headers)
# print(data.json())
tasks = [{'id': i['id'], 'name': i['name'], 'time': i['duration'], 'user': i['assigneeIds']} for i in data.json()]

user_id = tasks[0]['user'][0]
data = requests.get(
    f'https://api.clockify.me/api/v1/workspaces/{os.environ.get("WORKSPACE_ID")}/user/{user_id}/time-entries',
    headers=headers)

show_list = []
columns = ['Time', 'Task']

time_entries = data.json()
for task in tasks:
    task_id = task['id']
    task_times = list(filter(lambda x: x['taskId'] == task_id, time_entries))
    t_times = []
    for i in task_times:
        t_times.append({'date': i['timeInterval']['start'],
                        'time': i['timeInterval']['duration'] if 'duration' in i[
                            'timeInterval'] else None})
    dates = {}
    for item in t_times:
        if item['time'] is None:
            continue
        d = item['date'].split('T')[0]
        t = item['time'].replace('PT', '')
        mins = int(t[:t.find('M')]) if 'M' in t else 0
        secs = int(t[t.find('M') + 1:t.find('S')])
        if d in dates:
            dates[d] += secs + mins * 60
        else:
            dates[d] = secs + mins * 60

    t = '\n'.join([f'{date}: {time // 60}min{time % 60}sec' for date, time in dates.items()])
    show_list.append([t, task['name']])

# for i in show_list:
#     print(i)

print(tabulate(show_list, headers=columns))

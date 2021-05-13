# Daily_CLI_reporter

## Requirements
* requests == 2.25.1
* tabulate == 0.8.9

## Configuration
1. Go to `clockify.me/user/settings`, generate you API key and add it to config file.
2. Go to `clockify.me/workspaces/`, click `settings`. Now your address bar will look like `clockify.me/workspaces/{workspace_id}/settings`, copy `workspace_id` and add it to config file.

## Usage
To start utility type in console: 
```
python main.py [name of your project]
```
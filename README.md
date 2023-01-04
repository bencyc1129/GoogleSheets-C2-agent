GoogleSheets-C2-agent

The C2 agent that using google sheets to control victim host.

# Workflow
1. The attacker edits the sheet file **commands** in **2022CNProject@gmail.com**'s google drive, each line in first column of the sheet is a command.
2. The agent fetches the sheet file in csv format, saves as file called **commands**
3. The agent reads **commands** and parses the content as commands.
4. The agent executes the commands line by line, then writes stdin, stderr to **output.txt**.
5. The agent uploads **output.txt** to **2022CNProject@gmail.com**'s google drive.
6. The agent goes to sleep.

# Usage
## python script
1. `> pip install gdown google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client`
2. `> python agent.py`

## executable binary
- windows<br>
`> agent.exe`
- linux<br>
`> ./agent`

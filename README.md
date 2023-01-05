GoogleSheets-C2-agent

The C2 agent that using google sheets to control the victim host.

# Prerequisite
1. Google account. In this project I use **2022cnproject@gmail.com/cn2022project**.
2. A GCP project which activates Google drive API. In this project I named the project **CNProject2022**
3. Add test user into GCP project. In this project I only add **2022cnproject@gmail.com**.
4. Download **credentials.json** of your GCP project.
5. `> pip install gdown google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client`

# Workflow
1. The attacker edits the sheet file **commands** in **2022cnproject@gmail.com**'s google drive, each line in first column of the sheet is a command.
2. The agent fetches the sheet file in csv format, saves as file called **commands**
3. The agent reads **commands** and parses the content.
4. The agent executes the commands line by line, then writes stdout, stderr to **output.txt**.
5. The agent uploads **output.txt** to **2022cnproject@gmail.com**'s google drive.
6. The agent goes to sleep.

# Usage
The default access token is a null string, it's invalid for Google API, therefore the result of commands will not be uploaded or updated. You should use **tokenGen.py** to generate access token first, then add **token {access_token}** into sheet file in order to update the access token which agent uses remotely.

## Generate access token
Generate **token.json** then upload it to Google drive.
1. Make sure **credentials.json** is in the same directory with **tokenGen.py**.
2. `python tokenGen.py`

## C2 agent
Start the C2 agent.

### python script
- `> python agent.py`

### wrapped executable
- Windows<br>
`> agent.exe`
- Linux<br>
`> ./agent`

# feature
## die
If the command is **die**, the agent will kill itself immediately.

## sleep {sec}
If the command is **sleep {sec}**, the agent will update the specified sleep interval.

## token {access_token}
If the command is **token {access_token}**, the agent will update the specified access token

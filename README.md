# Development Phase Setup
Before cloning the repository and proceeding, make sure:
- You have [Git](https://git-scm.com/downloads), [VSCode](https://code.visualstudio.com/download), [Python 3.x](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/en/download/package-manager) already installed in your OS. 
- Your terminal's path is set to the desktop or your workspace.
## 1. Clone the Repository
${\textsf{\color{#aaffff}Windows (PowerShell):}}$
```md
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser; git clone https://github.com/m-a-y-h/nekon.git; cd nekon; $vscodePath = Get-ChildItem "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin" -Recurse -Filter "code.cmd" | Select-Object -ExpandProperty DirectoryName; if ($vscodePath) { if ($env:Path -notlike "*$vscodePath*") {[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$vscodePath", [System.EnvironmentVariableTarget]::User); Write-Host "VS Code path added to PATH." } else {Write-Host "VS Code path is already in PATH.";} } else { Write-Host "VS Code installation not found." }; code . -n
```
NOTE: If the CLI shows "VS Code installation not found" and you do have VSCode installed, you may need to manually open this folder with VS Code.

${\textsf{\color{#ffbfaa}Linux and MacOS (UNIX-bash):}}$
```bash
git clone https://github.com/m-a-y-h/nekon.git && cd nekon && code . -n
```

## 2. Setting Up the Backend:
Open a new Terminal in VSCode using ``Ctrl`` + ``Shift`` + `` ` ``
### Create a new Virtual Environment using PIP
${\textsf{\color{#aaffff}Windows (PowerShell):}}$
```md
py -m venv dpr; .\dpr\Scripts\Activate.ps1
```
${\textsf{\color{#ffbfaa}Linux and MacOS (UNIX-bash):}}$
```bash
python3 -m venv dpr && ln -s "$(pwd)/dpr/bin/python3" "$(pwd)/dpr/bin/py" && source dpr/bin/activate
```
### Install the Necessary Packages
${\textsf{\color{#aaffff}Windows (PowerShell):}}$
```
py -m pip install --upgrade pip; py -m pip install -r requirements.txt
```
${\textsf{\color{#ffbfaa}Linux and MacOS (UNIX-bash):}}$
```bash
py -m pip install --upgrade pip && py -m pip install -r requirements.txt
```

## 3. Setting Up the Frontend:
### Install Node Modules
${\textsf{\color{#aaffff}Windows (PowerShell):}}$
```
cd frontend; npm install; npm fund; cd ..
```
${\textsf{\color{#ffbfaa}Linux and MacOS (UNIX-bash):}}$
```bash
cd frontend && npm install && npm fund && cd ..
```
## 4. Git Configurations

### Configuring Git
Go to your Desktop and run the following commands in a global terminal, remember to edit the values:

${\textsf{\color{#aaffff}Windows (PowerShell):}}$
```
git config --global user.email "your-github-email@example.com"; git config --global user.name "Your Github Name or Username"; \
git config --global core.editor "code --wait"
```

${\textsf{\color{#ffbfaa}Linux and MacOS (UNIX-bash):}}$
```bash
git config --global user.email "your-github-email@example.com" && git config --global user.name "Your Github Name or Username" && \
git config --global core.editor "code --wait"
```

Finally, after making changes to the project files in your [branch](https://www.w3schools.com/git/git_branch.asp), commit and push it to the repository and [submit](https://github.com/m-a-y-h/nekon/pulls) a [pull request](https://www.w3schools.com/git/git_remote_send_pull_request.asp) for review.

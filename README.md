# Development Phase Setup

Make sure you have the following installed:
- [Git](https://git-scm.com/downloads)
- [VSCode](https://code.visualstudio.com/download)
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/package-manager)

## 1. Configuring Git
Configure Git globally if you haven't done so already; carefully edit and run the following commands in your terminal (one by one):
```bash
git config --global user.email "your-github-email@example.com"
git config --global user.name "Your Github Name or Username"
git config --global core.editor "code --wait"
```

## 2. Clone the Repository
Make sure that your terminal's path is set to your Desktop or a preferred workspace:
```bash
git clone https://github.com/m-a-y-h/nekon.git
```

## 3. Run the Setup Script
```bash
python nekon/setup.py
```
This script will:
1. Create and activate the virtual environment.
2. Install the required Python packages from `requirements.txt`.
3. Set up the frontend modules with `npm install`.
4. Generate the `.nekon` backend security configuration file.
5. Open the project for you in a new VSCode window.

> **Note:** You will need to replace the placeholder values in `.nekon` with your actual sensitive information, such as:
> - `SECRET_KEY` for Django
> - Database credentials (`RDS_HOST`, `RDS_PORT`, etc.)
> - OAuth configurations (`GOOGLE_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, etc.)

## 4. Final Steps
- Once you have the .nekon file ready. Run `cd backend` and `py manage.py migrate`.
- Finally, after making changes to the project files in your [branch](https://www.w3schools.com/git/git_branch.asp), commit and push it to the repository and [submit](https://github.com/m-a-y-h/nekon/pulls) a [pull request](https://www.w3schools.com/git/git_remote_send_pull_request.asp) for review.
# Development Phase Setup

Make sure you have the following installed:
- [Git](https://git-scm.com/downloads) | `git --version`
- [VSCode](https://code.visualstudio.com/download) | `code --version`
- [Python 3.x](https://www.python.org/downloads/) | `python -V` and `pip -V`
- [Node.js](https://nodejs.org/en/download/package-manager) | `node -v` and `npm -v`
> **Note:** On Windows, `code --version` command might not work if you didn't let it set its system environment variable during installation.
## 1. Configuring Git
Configure Git globally if you haven't done so already; carefully edit and run the following commands in your terminal (one-by-one):
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
The script is only compatible with Powershell, CMD, and UNIX bash:
```bash
python nekon/setup.py
```
This script will:
1. Create and activate the virtual environment.
2. Enable UNIX bash terminal users to use the short **py** prefix inside the virtual environment.
3. Install the required Python packages from `requirements.txt`.
4. Set up the frontend modules with `npm install`.
5. Generate the `.nekon` backend security configuration file.
6. Open the project for you in a new VSCode window.

> **Note:** You will need to replace the placeholder values in `.nekon` with your actual sensitive information. Here's how to get each credential:
> - A simple way to get yourself a [secret key](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY) for your project is by creating an entirely new django project in another directory, copying its SECRET_KEY value from settings.py and assigning it to `SECRET_KEY` in the .nekon file. You may now delete the other project you had created.
> - Sign-in into your [AWS account](https://console.aws.amazon.com/console/home?nc2=h_ct&src=header-signin) and create a [PostgreSQL database using the RDS service](https://www.w3schools.com/django/django_db_create_aws_account.php). Once you're done, head over to .nekon and update the values of `RDS_HOST`, `RDS_PORT`, `RDS_DBNAME`, `RDS_USER`, and `RDS_PASSWORD`.
> - Register your [Google Oauth App](https://developers.google.com/identity/protocols/oauth2) for `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
> - Register your [Github Oauth App](https://github.com/settings/applications/new) for `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`.

## 4. Final Steps
- Once you have the .nekon file ready. Run `cd backend` and `py manage.py migrate`.
- Finally, after making changes to the project files in your [branch](https://www.w3schools.com/git/git_branch.asp), commit and push it to the repository and perhaps ... [submit](https://github.com/m-a-y-h/nekon/pulls) a [pull request](https://www.w3schools.com/git/git_remote_send_pull_request.asp) for review I guess ...

> **Note:** In case your request times out each time you run `py manage.py migrate`, head over to your AWS console, search 'Security Groups', and then choose '**Security Groups - VPC feature**'. Now click on the Security group ID corresponding to the Security group name that your database is using. Find '**Edit inbound rules**' and then add a rule with **Type: `All Traffic`** & **Source:`Anywhere-IPv4`**.

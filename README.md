# GitHubScan

### Purpose: 
is to fetch git hub alerts of each repository and update the Geckoboard dataset for each team with repository of their intereste

### Approach:
- filter out archived repository
- classify the repository with write access for each team as repository of interest
- get github vulnerability alters count for each repository
- create dataset for each team on gecko board , which can be used to create the dashboard

### Environment Varibales
```bash
DEBUG=True
SECRET_KEY=<django-secret-key>
DATABASE_NAME=github.sqlite3
ORG_NAME=uktrade
GITHUB_TOKEN=<git-hub-token>
GITHUB_API_URL="https://api.github.com/graphql"
GECKO_TOKEN=<gecko-board-token>
SKIP_TOPIC='skip-vulnerability-scan'
```

### Commands
Update vulnerability db
```bash
$python manage.py run_update
```
Push updates to Geckoboard
```bash
$python manage.py run_report
```
Update vulnerability db and , push updates to Geckoboard
```bash
$python manage.py run_update_and_report
```

### Prerequisites
- Enable Graph dependency in github 
- Enable Aleters in github 

### Feature
- **Overview board:** showing top 20
- '++' after team name indicates there are more than one team associated with repository
- A seperate board for each team ( basedon github teams)
- **Skip scan:** if topic 'skip-vulnerability-scan' is found on repo , it will skip running vulnerability scan and displaying it on board
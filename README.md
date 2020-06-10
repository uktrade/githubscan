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
{
  "ALLOWED_HOSTS": "*",
  "DEBUG": "False",
  "EMAIL_REPORT_TO": "email1@domain.com,email2@anotherdomain.com",
  "GECKO_TOKEN": "<GECKO_TOKEN>",
  "GITHUB_API_URL": "https://api.github.com/graphql",
  "GITHUB_TOKEN": "<GITHUB_TOKEN>",
  "NOTIFY_API_KEY":"<GDS_NOTIFY_APIKEY>",
  "NOTIFY_TEMPLATE_ID": "<GDS_NOTIFY_TEMPLATEID>",
  "ORG_NAME": "<GITHUB_ORG>",
  "SECRET_KEY": "<DJANGO_SECRET_KEY>",
  "SKIP_TOPIC": "skip-vulnerability-scan"
}
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
Send report to EMAIL_REPORT_TO specified in environment variables
```bash
$python manage.py email_report
```
Send report to team admins, as specefied in github team table
```bash
$python manage.py email_teamAdmin
```

### Prerequisites
- Enable Graph dependency in github 
- Enable Aleters in github 

### Feature
- **Overview board:** showing top 20
- '++' after team name indicates there are more than one team associated with repository
- A seperate board for each team ( basedon github teams)
- **Skip scan:** if topic 'skip-vulnerability-scan' is found on repo , it will skip running vulnerability scan and displaying it on board
- send consolidated report of all the vulnurable repository in github organisation to team ( such as security team ) specified in EMAIL_REPORT_TO
- send team specific reports to team admin, as specified in  githubteam table (This needs to be done manually by member of WebOps at the moment).

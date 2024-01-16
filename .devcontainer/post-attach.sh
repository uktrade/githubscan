clear

BLUE='\033[0;34m'
GREY='\033[0;30m'
WHITE='\033[0;37m'
COLOUR_END='\033[0m'

PYTHON_VERSION=$(python --version | sed 's/[[:space:]|[:alpha:]]//g')
POSTGRES_VERSION=$(psql -h githubscan_db -U root githubscan -c "SHOW server_version;"  | grep -i pgdg | cut -d' ' -f2 |  sed 's/[[:space:]|[:alpha:]]//g')
PRECOMMIT_VERSION=$(pre-commit --version| sed 's/[[:alpha:]|[:space:]|-]//g')

printf "${BLUE}Github Scan Devcontainer:${COLOUR_END}\n"
printf "${GREY}Python:${COLOUER_END} ${WHITE}$PYTHON_VERSION${COLOUR_END}\n"
printf "${GREY}Postgres:${COLOUER_END} ${WHITE}$POSTGRES_VERSION${COLOUR_END}\n"
printf "${GREY}Pre-commit:${COLOUER_END} ${WHITE}$PRECOMMIT_VERSION${COLOUR_END}\n"

printf "${GREY}Starting Celery:${COLOUER_END}"

celery -A config worker -l debug

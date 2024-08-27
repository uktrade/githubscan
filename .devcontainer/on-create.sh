#!/bin/bash

function install_packages(){
    # install_packages
    #  - install bash-completion required to use poetry bash-completion
    # - install psql client
    apt-get update -y && apt-get install -y  bash-completion postgresql-client locales &&   apt-get autoremove -y && apt-get autoclean
    locale-gen en_US.UTF-8
    update-locale

    echo 'source /etc/profile' >> ${HOME}/.bashrc

}

function install_poetry(){
    # install_poerty()
    # - installs latest version of poetry
    # - installs command completion for poetry
    pip install poetry
    poetry completions bash > /etc/bash_completion.d/poetry
    poetry self add poetry-plugin-up
    poetry self add poetry-plugin-export
    echo 'source $(poetry env info --path)/bin/activate' >> ${HOME}/.bashrc
}

setup_precommit(){
    source ${HOME}/.bashrc
    pre-commit autoupdate
    pre-commit install
}

init_project(){
    source ${HOME}/.bashrc
    python manage.py makemigrations && python manage.py migrate
}



function configure_git(){
    # this configure_git
    # - sets vscode as default editor for git
    # - sets git username if set in the .env file
    #  - sets git email if set in the .env file
    git config --global core.editor "code -w"

    if [ !  -z "${GIT_USER_NAME}" ]
    then
        git config --global user.name "${GIT_USER_NAME}"
    fi

    if [ !  -z "${GIT_EMAIL}" ]
    then
        git config --global user.email "${GIT_EMAIL}"
    fi
}

function install_git_bash_prompt(){
    # install_git_bash_prompt
    #  - install git bash prompt
    #  - configure git bash propmpt
    #  - enable git bash prompt
    if [ ! -d "${HOME}/.bash-git-prompt" ]
    then
        git clone https://github.com/magicmonty/bash-git-prompt.git  ${HOME}/.bash-git-prompt --depth=1

        echo 'if [ -f "${HOME}/.bash-git-prompt/gitprompt.sh" ]; then
        GIT_PROMPT_ONLY_IN_REPO=1
        source "$HOME/.bash-git-prompt/gitprompt.sh"
fi' >> ${HOME}/.bashrc

    fi
}

function install_poetry_packages(){
    # install poerty packages
    # - configure poetry to create virtual env with in project so that vscode can find python interpreter
    # - check if project file exist

    poetry config virtualenvs.in-project true


    if [ -f "poetry.lock" ]
    then
        poetry lock
    fi


    if [ -f "pyproject.toml" ]
    then
        poetry up
        poetry install
    fi
}

function main(){
    # main
    #  - execute functions in a given order

    install_packages
    install_git_bash_prompt
    configure_git
    install_poetry
    install_poetry_packages

    setup_precommit
    init_project

}

# call to main
main

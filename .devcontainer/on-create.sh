install_psql_client(){
    apt-get update -y
    apt-get install -y postgresql-client locales
    apt-get autoremove -y
    apt-get autoclean
    locale-gen en_US.UTF-8
    update-locale
}

install_python_packages(){
    pip install --root-user-action=ignore --upgrade pip
    pip install --root-user-action=ignore pip-tools pre-commit

    pip-compile --resolver=backtracking requirements-dev.in
    pip-compile --resolver=backtracking requirements.in
    pip install --root-user-action=ignore -r requirements-dev.txt
}

setup_precommit(){
    pre-commit autoupdate
    pre-commit install
}

init_project(){
    python manage.py migrate
}

intall_git_bashprompt(){
    git clone https://github.com/magicmonty/bash-git-prompt.git $HOME/.bash-git-prompt --depth=1

    echo -e "if [ -f "$HOME/.bash-git-prompt/gitprompt.sh" ]
then
    GIT_PROMPT_ONLY_IN_REPO=1
    source $HOME/.bash-git-prompt/gitprompt.sh
fi\n" >> $HOME/.bashrc

}

configure_git(){

    if [[ ! -z $GIT_USER_NAME && ! -z $GIT_EMAIL && ! -z $GIT_COMMIT_EDITOR ]]
    then
        git config --global user.name "$GIT_USER_NAME"
        git config --global user.email "$GIT_EMAIL"
        git config --global --replace-all core.editor "$GIT_COMMIT_EDITOR"
    else
        echo "Skipping git configuration, one or more GIT variable is not set"
    fi
}

main(){
    intall_git_bashprompt
    configure_git
    install_psql_client
    install_python_packages
    setup_precommit
    init_project
}

main

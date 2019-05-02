from django.conf import settings
import requests
import os
import json


class Info:

    HEADERS = {
        "Authorization": "token " + settings.GITHUB_TOKEN,
        "Content-Type": "application/json",
    }

    ORG_NAME = settings.ORG_NAME
    APP_ROOT = settings.BASE_DIR
    GITHUB_API_URL = settings.GITHUB_API_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.verify = False
        self.first = 10

    def __openQuery(self, file):
        query = (open(file, 'r', encoding='unicode_escape')).read().splitlines()
        return "".join(str(x) for x in query)

    def __GithubResponse(self, payload):
        return self.session.post(
            self.GITHUB_API_URL, data=payload)

    def getTeams(self):
        teams = dict()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'teams.gql'))
        query_variables = {"org_name": self.ORG_NAME, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()
        while True:
            for edge in response['data']['organization']['teams']['edges']:
                if edge['node']['name'] != "default":
                    teams[edge['node']['id']] = (
                        edge['node']['name']).replace(' ', '-').lower()
            if response['data']['organization']['teams']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['teams']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(payload=data)).json()

        return teams

    def getRepos(self):
        repos = dict()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'repos.gql'))
        query_variables = {"org_name": self.ORG_NAME, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            for edge in response['data']['organization']['repositories']['edges']:
                if not edge['node']['isArchived']:
                    repos[edge['node']['id']] = edge['node']['name']
            if response['data']['organization']['repositories']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['repositories']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(payload=data)).json()

        return repos

    def getVulnerabilityAlerts(self, repository):
        SERVERITY_COUNT = {'low': 0, 'moderate': 0, 'high': 0, 'critical': 0}

        self.session.headers.update(
            {'Accept': 'application/vnd.github.vixen-preview+json'})
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'vulnerabilityAlerts.gql'))
        query_variables = {"org_name": self.ORG_NAME,
                           "repo_name": repository, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            for node in response['data']['organization']['repository']['vulnerabilityAlerts']['nodes']:
                severity = (node['securityVulnerability']['severity']).lower()
                SERVERITY_COUNT[severity] = +1
            if response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(payload=data)).json()

        return {repository: SERVERITY_COUNT}

    def getTeamRepos(self, team):
        teamrepos = list()

        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'teamRepo.gql'))
        query_variables = {"org_name": self.ORG_NAME,
                           "team": team, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            for edge in response['data']['organization']['team']['repositories']['edges']:
                if not edge['node']['isArchived'] and (edge['permission'] == 'WRITE' or edge['permission'] == 'ADMIN'):
                    teamrepos.append(edge['node']['name'])

            if response['data']['organization']['team']['repositories']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['team']['repositories']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(
                    payload=data)).json()

        return teamrepos

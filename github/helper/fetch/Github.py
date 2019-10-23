from django.conf import settings
from operator import itemgetter
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
        teams = list()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'teams.gql'))
        query_variables = {"org_name": self.ORG_NAME, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()
        while True:
            for edge in response['data']['organization']['teams']['edges']:
                if edge['node']['name'] != "default":
                    teams.append(
                        (edge['node']['name']).replace(' ', '-').lower())
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
        repos = list()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'repos.gql'))
        query_variables = {"org_name": self.ORG_NAME, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            for edge in response['data']['organization']['repositories']['edges']:
                if not edge['node']['isArchived']:
                    repos.append(edge['node']['name'])
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
                if node['dismissedAt'] is None:
                    severity = (node['securityVulnerability']
                                ['severity']).lower()
                    SERVERITY_COUNT[severity] += 1

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

    def getRepoTopics(self, repository):
        topics = list()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'repoTopics.gql'))
        query_variables = {"org_name": self.ORG_NAME,
                           "repo_name": repository, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:

            edges = response['data']['organization']['repository']['repositoryTopics']['edges']

            if edges:
                for edge in edges:
                    topics.append(edge['node']['topic']['name'])

            if response['data']['organization']['repository']['repositoryTopics']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['repository']['repositoryTopics']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(
                    payload=data)).json()

        return topics

    def getVulnerabilityDetails(self, repository):

        report = dict()
        severities = list()

        self.session.headers.update(
            {'Accept': 'application/vnd.github.vixen-preview+json'})
        query = self.__openQuery(os.path.join(
            self.APP_ROOT, 'github', 'gqlQueries', 'vulnerabilityAlerts.gql'))
        query_variables = {"org_name": self.ORG_NAME,
                           "repo_name": repository, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            nodes = response['data']['organization']['repository']['vulnerabilityAlerts']['nodes']
            # Lets not try to loop if it is None ( i.e. no Servrity exits)
            if nodes:
                for node in nodes:
                    cve = None
                    if node['dismissedAt'] is None:
                        severity = (node['securityVulnerability']
                                    ['severity']).lower()

                        package_name = node['securityVulnerability']['package']['name']
                        cve_identifier = dict()
                        has_cve_identifier = False
                        cve_url = None
                        for identifier in node['securityAdvisory']['identifiers']:
                            if identifier['type'].lower() == 'cve':
                                has_cve_identifier = True
                                cve_identifier = identifier

                        if has_cve_identifier:
                            identifier_type = cve_identifier['type']
                            identifier_value = cve_identifier['value']
                            if len(node['securityAdvisory']['references']) > 1:
                                cve_url = node['securityAdvisory']['references'][1]['url']
                            else:
                                cve_url = node['securityAdvisory']['references'][0]['url']

                        else:
                            identifier_type = node['securityAdvisory']['identifiers'][0]['type']
                            identifier_value = node['securityAdvisory']['identifiers'][0]['value']

                        severities.append((
                            package_name, severity, identifier_type, identifier_value, cve_url),)

                if not response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['hasNextPage']:
                    break
                else:
                    query_variables.update(
                        {"after": response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['endCursor']})
                    data = json.dumps(
                        {"query": query, "variables": query_variables})
                    response = (self.__GithubResponse(payload=data)).json()

            else:
                break

        sorted_severities = sorted(severities, key=itemgetter(1))
        return set(sorted_severities)

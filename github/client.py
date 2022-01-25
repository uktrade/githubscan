from django.conf import settings
from operator import itemgetter
from collections import Counter

import requests
import os
import json


class GHClient:

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
        self.first = settings.FIRST_N_RECORDS

    def __openQuery(self, file):
        query = (open(file, 'r', encoding='unicode_escape')).read().splitlines()
        return "".join(str(x) for x in query)

    def __GithubResponse(self, payload):
        return self.session.post(
            self.GITHUB_API_URL, data=payload)

    def getRepos(self):
        """ Retrieve a list of all non-archived repositories owned by the
        organisation (settings.ORG_NAME).
        """

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

    def getRepoTopics(self, repository):
        """ Retrieve all topics for a repo.
        """
        topics = list()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT,  'github', 'gqlQueries', 'repoTopics.gql'))
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

    def getTeams(self):
        """ Retrieve a list of all Github teams belonging to the organisation
        (settings.ORG_NAME).
        """
        teams = list()
        query = self.__openQuery(os.path.join(
            self.APP_ROOT,  'github', 'gqlQueries', 'teams.gql'))
        query_variables = {"org_name": self.ORG_NAME, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()
        while True:
            for edge in response['data']['organization']['teams']['edges']:
                teams.append((edge['node']['name']).replace(' ', '-').lower())
            if response['data']['organization']['teams']['pageInfo']['hasNextPage'] is False:
                break
            else:
                query_variables.update(
                    {"after": response['data']['organization']['teams']['pageInfo']['endCursor']})
                data = json.dumps(
                    {"query": query, "variables": query_variables})
                response = (self.__GithubResponse(payload=data)).json()

        return teams

    def getTeamRepos(self, team):
        """ Retrieve a list of all repositories for a Github team.
        """
        teamrepos = list()

        query = self.__openQuery(os.path.join(
            self.APP_ROOT,  'github', 'gqlQueries', 'teamRepo.gql'))
        query_variables = {"org_name": self.ORG_NAME,
                           "team": team, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            for edge in response['data']['organization']['team']['repositories']['edges']:
                if not edge['node']['isArchived'] and (edge['permission'] == 'WRITE' or edge['permission'] == 'ADMIN' or edge['permission'] == 'MAINTAIN'):
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

    def getVulnerabilityAlerts(self, repository):
        """ Retrieve a list of vulnerability alerts, sorted by level of
        severity.
        """

        severities = list()

        self.session.headers.update(
            {'Accept': 'application/vnd.github.vixen-preview+json'})
        query = self.__openQuery(os.path.join(
            self.APP_ROOT,  'github', 'gqlQueries', 'vulnerabilityAlerts.gql'))
            
        query_variables = {"org_name": self.ORG_NAME,
                           "repo_name": repository, "first": self.first}

        data = json.dumps({"query": query, "variables": query_variables})

        response = (self.__GithubResponse(payload=data)).json()

        while True:
            nodes = response['data']['organization']['repository']['vulnerabilityAlerts']['nodes']
            # Lets not try to loop if it is None ( i.e. no Servrity exits)
            if nodes is not None:
                for node in nodes:                    
                    if node['dismissedAt'] is None:
                        severity = (node['securityVulnerability']
                                    ['severity']).lower()
                        package_name = node['securityVulnerability']['package']['name']
                        ghsa_identifier = dict()

                        ghsaId = node['securityAdvisory']['ghsaId']
                        refrences = node ['securityAdvisory']['references']
                        identifiers = node['securityAdvisory']['identifiers']

                        identifier_type = identifiers[0]['type']
                        identifier_value = identifiers[0]['value']                            
                        refrence_url = refrences[0]

                        if ghsaId:
                            for id in identifiers:
                                if id['type'] == 'GHSA':
                                    identifier_type  = id['type']
                                    identifier_value = id['value']
                                    break

                            for ref in refrences:
                                if ghsaId == ref['url'].split('/')[-1]:
                                    refrence_url = ref['url']
                                    break                      

                        published_at = node['securityAdvisory']['publishedAt']

                
                        patched_version = 'Not Known'

                        if node['securityVulnerability']['firstPatchedVersion'] is not None:
                            patched_version = node['securityVulnerability']['firstPatchedVersion']['identifier']

                        severities.append((
                            package_name, severity, identifier_type, identifier_value, refrence_url, published_at,patched_version))

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

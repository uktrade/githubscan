# -*- coding: utf-8 -*-
from scanner import GHAPIClient, GHQueryBuilder
import re
from pathlib import Path
import logging
from copy import deepcopy
from common.functions import isinstance_of

logger = logging.getLogger(__name__)


class GHQueryExecutor:

    """
    A class to execute Github GraphQL queries using GHAPIClient

    Attributes:
    ------------
    QUERY_DIRECTORY: PosixPath. It points to the directory where all graphql queries are stored
    """

    QUERY_DIRECTORY = Path.joinpath(Path(__file__).resolve().parent, "queries")

    def __init__(self):
        """
        It initalizes API Client and class variables , also raises/logs error if initalization fails

        Parameters:
        -----------
        end_point: str. it must be a valid url of api end point being used
        verify_ssl: bool. It must be a boolen value suggesting if we are using ssl or non-ssl connection. defaults to True

        Variables:
        ----------
        self._gh_api_client: GHAPIClient() init Github API Client
        self._query_text: str. GraphQL query string ( normally loaded from a file )
        self._teams: list
        self._repositories_and_alerts = [{}] , list of dict for details refer to schema
        self._teams_repositories = [] , list of repositories on which team has ADMIN | MAINTAINER | WRITE permision
        """

        self._api_client = None
        self._query_builder = None
        self._teams = []
        self._repositories_and_alerts = []
        self._teams_repositories = []

    def clear(self):
        """A method to clear all class variables"""
        self._api_client = None
        self._query_builder = None
        self._teams = []
        self._repositories_and_alerts = []
        self._teams_repositories = []

    def __del__(self):
        """A class destructor"""
        self.clear()

    @property
    def api_client(self):
        isinstance_of(self._api_client, GHAPIClient, "api_client")
        return self._api_client

    @api_client.setter
    def api_client(self, api_client_obj):
        isinstance_of(api_client_obj, GHAPIClient, "api_client")
        self._api_client = api_client_obj

    @property
    def query_builder(self):
        isinstance_of(self._query_builder, GHQueryBuilder, "query_builder")
        return self._query_builder

    @query_builder.setter
    def query_builder(self, query_builder_obj):
        isinstance_of(query_builder_obj, GHQueryBuilder, "query_builder")
        self._query_builder = query_builder_obj

    """
    Note: Methods below are not well tested. reason being github fetch very much dynamic data and, we would find it impoosible to test with real data when
     - github team names may change
     - github team may be deleted
     - repositories name may change
     - repository might get archived
     - repository might get deleted
    """

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams_query(self, payload):
        """
        Exceuctes query and fetches all the team

        Parameters:
        -----------
        payload: dict, { query: "valid github graphQL query", "variables": dict }

        Returns:
        ---------
        None

        Variables:
        -----------
        it sets self._teams
        """

        while True:
            self.query_builder.make_gql_query_from_dict = payload
            self.query_builder.is_a_valid_input_query(payload=payload, caller="teams")
            self.api_client.post_query = self.query_builder.gql_query

            data = (self.api_client.post_response.json())["data"]
            teams_info = data["organization"]["teams"]["teams_info"]
            pageInfo = data["organization"]["teams"]["pageInfo"]

            for info in teams_info:
                """
                Github does not like team names with space and replaces it with a '-' behind the scene (as noted in team name URL)
                if we do not substitute , we will get incorrect results
                """
                team_name = info["name"].replace(" ", "-")
                self._teams.append(team_name.lower())

            if not pageInfo["hasNextPage"]:
                break

            payload["variables"].update({"after": pageInfo["endCursor"]})

    @property
    def repositories_and_alerts(self):
        return self._repositories_and_alerts

    @repositories_and_alerts.setter
    def repositories_and_alerts_query(self, payload):
        """
        Exceuctes query and fetches all repositories , their topics and alerts

        Parameters:
        -----------
        payload: dict, { query: "valid github graphQL query", "variables": dict }

        Returns:
        ---------
        None

        Variables:
        -----------
        it sets self._repositories_and_alerts

        CAUTION:
        ---------
        For this method, query string must replace variable {$user} with Github Login
        Which  needs to be done by actual caller/user of the method before setting payload
        """

        while True:
            self.query_builder.make_gql_query_from_dict = payload
            self.query_builder.is_a_valid_input_query(
                payload=payload, caller="repositories_and_alerts_query"
            )
            self.api_client.post_query = self.query_builder.gql_query

            data = (self.api_client.post_response.json())["data"]

            repositories_info = data["repositories"]["repositories_info"]
            pageInfo = data["repositories"]["pageInfo"]

            for info in repositories_info:
                repository_name = info["name"]
                topics = info["repository_topics_info"]["topics"]
                alerts = info["repository_alerts_info"]["alerts"]

                """
                if repository has topic , make it into list
                """
                if topics:
                    topics = [x["topic"]["name"] for x in topics]

                """
                We can skip all work if there is no alert found
                """
                if alerts:
                    """
                    We are going to update and modify the default alerts struct slightly to process this data slightly more easily
                    alert = {
                        'id'
                        'createdAt'
                        'state'
                        'dismissedAt'
                        'level' #  meaning alaert level
                        'package' #meaning affacted package
                        'patched_version' #meaning first patched version
                        'advisory_url' #link to advisory url on vulnerability
                    }
                    it removes followinf original keys
                    - severity
                    - advisory
                    """

                    for alert in alerts:
                        package_name = alert["severity"]["package"]["name"]
                        alert_level = alert["severity"]["level"]

                        patched_version = "unknown"

                        if alert["severity"]["patched_version"]:

                            patched_version = alert["severity"]["patched_version"][
                                "identifier"
                            ]

                        advisory_urls_list = [
                            x["url"] for x in alert["advisory"]["urls"]
                        ]

                        advisory_url = ""

                        """
                        Match to github advisory as a first pref
                        """
                        github_advisory_regex = re.compile(
                            "https://github.com/advisories/*"
                        )
                        match = list(
                            filter(github_advisory_regex.match, advisory_urls_list)
                        )
                        if match:
                            advisory_url = match.pop()
                        else:
                            """
                            If Github advisory is not found, match to ndv.nist.gov
                            """
                            nist_regex = re.compile("https://nvd.nist.gov/*")
                            match = list(filter(nist_regex.match, advisory_urls_list))
                            if match:
                                advisory_url = match.pop()
                            else:
                                """
                                If nothing matches, simply pick the first from list
                                """
                                advisory_url = advisory_urls_list.pop()

                        alert.update({"level": alert_level})
                        alert.update({"package": package_name})
                        alert.update({"patched_version": patched_version})
                        alert.update({"advisory_url": advisory_url})

                        del alert["severity"]
                        del alert["advisory"]

                self._repositories_and_alerts.append(
                    {
                        "name": repository_name,
                        "topics": topics,
                        "alerts": alerts,
                        "teams": [],
                    }
                )

            if not pageInfo["hasNextPage"]:
                break

            payload["variables"].update({"after": pageInfo["endCursor"]})

    @property
    def teams_repositories(self):
        return self._teams_repositories

    @teams_repositories.setter
    def teams_repositories_query(self, payload):
        """
        Just a wrapper function so we can fetch repoistories for each and every team in org

        Parameters:
        -----------
        payload: dict, { query: "valid github graphQL query", "variables": dict }

        Depends On:
        -----------
        self.teams : i.e. teams_query must execute before you can use this method effectively
        """

        for index, team in enumerate(self.teams):
            print(f"processing:{team}")
            self._teams_repositories.insert(index, {team.lower(): []})
            self._team_repositories(team=team, index=index, payload=deepcopy(payload))

    def _team_repositories(self, team, index, payload):
        """
        Why We need this info?
        -----------------------
        We need to know which repositories alerts needs to be distributed to
        which team, that is the relation that this method builds

        Assumption:
        ------------
        While associating teams and repositories we assume Teams with one or
        more of following permissions are considered

         - ADMIN
         - MAINTAINER
         - WRITE

        The reasoning behind this is if team is only having 'READ' permission.
        They are not going to be able to contibute ( likely not interested either )
        anything which could fix the vulnerability

        Parameters:
        ------------
        team : name of the team for which we are going to run query
        index : index at which we need to update info
        payload: dict, { query: "valid github graphQL query", "variables": dict }

        Ideal Soltuion:
        ----------------
        Ideal solution is to have 'repositoryTeamConnection' so we can fetch
        associated teams directly from repositories query. However. there is
        not such a connection in github api v4,so we need to go other way
        around

        Optimization:
        -------------
        For optimum use of GraphQL Query we have does following
            - Sort by permission in decending order
            i.e. ADMIN , MAINTAINER,WRITE and READ
        Sorting allows us to exit loop as soon as we hit the first 'READ' permission
        knowing all following permission are 'READ'
        """

        while True:
            payload["variables"].update({"team": team.lower()})
            self.query_builder.make_gql_query_from_dict = payload
            self.query_builder.is_a_valid_input_query(
                payload=payload, caller="teams_repositories"
            )

            self.api_client.post_query = self.query_builder.gql_query

            data = (self.api_client.post_response.json())["data"]
            team_repositories_info = data["organization"]["team"]["team_repositories"][
                "edges"
            ]
            pageInfo = data["organization"]["team"]["team_repositories"]["pageInfo"]

            for repository_info in team_repositories_info:
                """
                If repo is archived or team does not have ADMIN,MAINTAINER or WRITE permission on repo, there is no need to record it
                """

                if repository_info["repository"]["isArchived"] or repository_info[
                    "permission"
                ] not in {
                    "ADMIN",
                    "MAINTAINER",
                    "WRITE",
                }:
                    continue

                self._teams_repositories[index][team.lower()].append(
                    repository_info["repository"]["name"]
                )

            if not pageInfo["hasNextPage"]:
                break

            payload["variables"].update({"after": pageInfo["endCursor"]})

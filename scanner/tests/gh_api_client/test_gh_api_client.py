# -*- coding: utf-8 -*-
from django.conf import settings

import json


def test_gh_client_with_invalid_query(real_test, gh_client, caplog):
    try:
        gh_client.url = settings.GITHUB_API_URL
        gh_client.auth_header = gh_client.token_auth_header
        gh_client.auth_token = settings.GITHUB_AUTH_TOKEN
        query_str = """{
                        organization(login:$login){
                            login
                            name
                            }
                        }
                    """
        query_variables = {"login": settings.GITHUB_LOGIN}
        gh_client.post_query = json.dumps(
            {"query": query_str, "variables": query_variables}
        )
        assert False
    except Exception:
        gh_client.clear()
        assert "Failed: Post Query Response status: 200" in caplog.messages
        assert True


def test_gh_client(real_test, gh_client, caplog):
    gh_client.url = settings.GITHUB_API_URL
    gh_client.auth_header = gh_client.token_auth_header
    gh_client.auth_token = settings.GITHUB_AUTH_TOKEN
    query_str = """
                query($login:String!){
                    organization(login:$login){
                        login
                        name
                        }
                    }
                """
    query_variables = {"login": settings.GITHUB_LOGIN}
    gh_client.post_query = json.dumps(
        {"query": query_str, "variables": query_variables}
    )
    content = json.loads(gh_client.post_response.content)
    login_name = content["data"]["organization"]["login"]
    organization_name = content["data"]["organization"]["name"]

    assert "Success: Post Query Response status: 200" in caplog.messages
    assert gh_client.post_response.status_code == 200
    assert settings.GITHUB_LOGIN == login_name
    assert settings.GITHUB_ORGANIZATION_NAME == organization_name

    gh_client.clear()

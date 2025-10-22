import base64
import uuid

import pytest
from django.core.cache import cache
from django.test import RequestFactory

from apps.core.exceptions.base_app_exception import UnauthorizedException
from apps.node_mgmt.utils.token_auth import check_token_auth, generate_node_token


@pytest.mark.django_db
def test_check_token_auth_derives_node_id_when_query_missing():
    cache.clear()
    node_id = uuid.uuid4().hex
    token = generate_node_token(node_id, "10.0.0.1", "tester")
    header = "Basic " + base64.b64encode(f"{token}:token".encode()).decode()

    request = RequestFactory().get("/api/v1/node_mgmt/open_api/node")
    request.META["HTTP_AUTHORIZATION"] = header

    validated_node_id = check_token_auth(None, request)

    assert validated_node_id == node_id
    assert request.META["sidecar_node_id"] == node_id


@pytest.mark.django_db
def test_check_token_auth_rejects_mismatched_node_id():
    cache.clear()
    node_id = uuid.uuid4().hex
    token = generate_node_token(node_id, "10.0.0.1", "tester")
    header = "Basic " + base64.b64encode(f"{token}:token".encode()).decode()

    request = RequestFactory().get("/api/v1/node_mgmt/open_api/node")
    request.META["HTTP_AUTHORIZATION"] = header

    with pytest.raises(UnauthorizedException):
        check_token_auth("other-node", request)


@pytest.mark.django_db
def test_check_token_auth_requires_token_header():
    cache.clear()
    request = RequestFactory().get("/api/v1/node_mgmt/open_api/node")

    with pytest.raises(UnauthorizedException):
        check_token_auth("missing", request)

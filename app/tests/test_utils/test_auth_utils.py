import pytest

from fastapi import Request, HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.utils.auth_utils import decode_jwt

client = TestClient(app)

def test_decode_jwt():
    # Test case 1: Valid request with valid token
    scope = {
        "type": "http",
        "method": "POST",
        "scheme": "http",
        "headers": [],
    }
    request = Request(scope=scope)
    request.cookies["token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcyNjI2Mzk1Nn0.YCfo55Li74DnbmwJi8hCAhb4XCb-X_qlDAGnBePQV7A"
    payload = decode_jwt(request)
    assert isinstance(payload, dict)

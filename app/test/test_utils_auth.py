import pytest
import os
import sys

proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..'))
if proj_dir not in sys.path:
    sys.path.append(proj_dir)

from app.utils.auth import verify_password, hash_password  # noqa


class TestHashPassword:
    def test_hash_password(self):
        password = 'secret'
        hashed_password = hash_password(password=password)

        assert hashed_password != password

        assert len(hashed_password) == 64

    def test_verify_password(self):
        password = 'secret'
        hashed_password = hash_password(password=password)

        assert verify_password(hashed_password, password) is True
        assert verify_password(hashed_password, 'qqq') is False

    def test_verify_password_invalid_key(self):
        password = 'secret'
        hashed_password = hash_password(password=password)
        hashed_password_word = hashed_password[:-1] + 'q'
        hashed_password_len = hashed_password[:-1]

        assert verify_password(hashed_password_word, password) is False
        assert verify_password(hashed_password_len, password) is False

from src.auth.hash import hash_password, verify_password
import pytest


def test_hash_password():
    password = "Password1/"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password)


def test_wrong_password():
    password = "Password1/"
    wrong_password = "WrongPassword1/"
    hashed_password = hash_password(password)

    assert not verify_password(wrong_password, hashed_password)


def test_wrong_hash():
    password = "Password1/"
    wrong_hash = "wronghash"

    with pytest.raises(Exception):
        verify_password(password, wrong_hash)


def test_hash_is_unique():
    password = "Password1/"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2


def test_verify_with_different_hashes():
    password = "Password1/"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
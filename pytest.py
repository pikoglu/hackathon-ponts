import pytest
from flask import Flask


@pytest.fixture
def client():
    Flask.config["TESTING"] = True
    with Flask.test_client() as client:
        yield client


def test_acces_page_accueil(client):
    reponse = client.get("/")
    # Vérifie que la page d'accueil renvoie un statut "200 OK"
    assert reponse.status_code == 200


def test_envoi_question_a_prompt(client):
    reponse = client.post("/prompt", data={"prompt": "Quelle est la couleur du ciel?"})
    # Vérifie que la route renvoie un statut "200 OK" et contient la clé "answer" dans la réponse JSON
    assert reponse.status_code == 200
    assert "answer" in reponse.get_json()


def test_obtenir_question(client):
    reponse = client.get("/question")
    # Vérifie que la route renvoie un statut "200 OK" et contient la clé "answer" dans la réponse JSON
    assert reponse.status_code == 200
    assert "answer" in reponse.get_json()


def test_envoi_question_et_reponse(client):
    reponse = client.post(
        "/answer", data={"question": "Quelle est la couleur du ciel?", "prompt": "Bleu"}
    )
    # Vérifie que la route renvoie un statut "200 OK" et contient la clé "answer" dans la réponse JSON
    assert reponse.status_code == 200
    assert "answer" in reponse.get_json()

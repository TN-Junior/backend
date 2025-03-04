import pytest
from app import app, db
from models.participant import Participant

@pytest.fixture
def client():
    with app.test_client() as client:
        # Cria um banco de dados temporário para os testes
        with app.app_context():
            db.create_all()
        yield client
        # Limpa o banco de dados após os testes
        with app.app_context():
            db.drop_all()

def test_create_participant(client):
    # Teste de criação de participante
    response = client.post('/participants', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'participation': 50
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Participant added successfully'
    assert data['participant']['firstName'] == 'John'

def test_get_participants(client):
    # Teste de obtenção de participantes
    client.post('/participants', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'participation': 50
    })
    response = client.get('/participants')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['firstName'] == 'John'

def test_invalid_participant(client):
    # Teste de criação com dados inválidos (sem nome)
    response = client.post('/participants', json={
        'firstName': '',
        'lastName': 'Doe',
        'participation': 50
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

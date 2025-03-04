import pytest
from app import create_app, db
from app.models import Participant

@pytest.fixture(scope='module')
def test_client():
    # Cria uma instância do aplicativo Flask para os testes
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Usando um banco de dados local (persistente)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Cria as tabelas no banco de dados
    with app.app_context():  # Garantindo que o código roda dentro do contexto da aplicação
        db.create_all()

    # Retorna o cliente de testes
    yield app.test_client()

    # Limpeza após os testes
    with app.app_context():
        db.drop_all()  # Limpa o banco após os testes




def test_create_participant(test_client):
    # Testa a criação de um participante no banco de dados
    with test_client.application.app_context():  # Certifica que a operação está no contexto da aplicação
        new_participant = Participant(
            first_name="John",
            last_name="Doe",
            participation=85
        )

        db.session.add(new_participant)
        db.session.commit()

        # Verifica se o participante foi salvo no banco
        participant = Participant.query.get(new_participant.id)
        assert participant is not None
        assert participant.first_name == "John"
        assert participant.last_name == "Doe"
        assert participant.participation == 85


def test_participant_retrieval(test_client):
    # Testa a recuperação de participantes do banco de dados
    with test_client.application.app_context():
        new_participant = Participant(
            first_name="Jane",
            last_name="Smith",
            participation=90
        )

        db.session.add(new_participant)
        db.session.commit()

        # Recupera o participante do banco
        participant = Participant.query.get(new_participant.id)
        assert participant.first_name == "Jane"
        assert participant.last_name == "Smith"
        assert participant.participation == 90


def test_participant_update(test_client):
    # Testa a atualização dos dados de um participante
    with test_client.application.app_context():
        new_participant = Participant(
            first_name="John",
            last_name="Doe",
            participation=75
        )

        db.session.add(new_participant)
        db.session.commit()

        # Atualiza o participante
        new_participant.first_name = "Johnny"
        new_participant.participation = 95
        db.session.commit()

        # Verifica se os dados foram atualizados corretamente
        participant = Participant.query.get(new_participant.id)
        assert participant.first_name == "Johnny"
        assert participant.participation == 95


def test_participant_deletion(test_client):
    # Testa a exclusão de um participante
    with test_client.application.app_context():
        new_participant = Participant(
            first_name="Mark",
            last_name="Twain",
            participation=70
        )

        db.session.add(new_participant)
        db.session.commit()

        # Exclui o participante
        db.session.delete(new_participant)
        db.session.commit()

        # Verifica se o participante foi excluído
        participant = Participant.query.get(new_participant.id)
        assert participant is None


def test_invalid_participant(test_client):
    # Testa a criação de um participante inválido (campo obrigatório)
    with test_client.application.app_context():
        try:
            # Tentando criar um participante com dados inválidos
            invalid_participant = Participant(
                first_name="",
                last_name="Doe",
                participation=120  # participação fora do intervalo válido
            )
            db.session.add(invalid_participant)
            db.session.commit()
            pytest.fail("Expected ValueError due to invalid data")
        except ValueError as e:
            assert str(e) == "First name and last name cannot be empty" or "Participation must be between 1 and 100"

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.database import Base


@pytest.fixture(autouse=True)
def mock_config_files(monkeypatch, tmp_path):
    # Создаем временный конфиг
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "user_settings.json"
    config_file.write_text('''{
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"]
    }''')

    # Мокаем путь к конфигу
    monkeypatch.setattr(
        "src.services.finance_api._get_config_path",
        lambda: config_file
    )


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_excel(tmp_path):
    data = {
        "Дата операции": ["31.12.2021 16:44:00"],
        "Дата платежа": ["31.12.2021"],
        "Номер карты": ["*7197"],
        "Статус": ["OK"],
        "Сумма операции": ["-160,89"],
        "Валюта операции": ["RUB"],
        "Кэшбэк": [""],
        "Категория": ["Супермаркеты"],
        "MCC": [5411],
        "Описание": ["Колхоз"],
        "Бонусы (включая кэшбэк)": ["3,00"],
        "Округление на инвесткопилку": ["0,00"],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_operations.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

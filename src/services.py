from typing import List, Dict
from datetime import datetime
import re
import logging
from .models import Transaction
import pandas as pd


logger = logging.getLogger(__name__)


def analyze_cashback(data: List[Transaction], year: int, month: int) -> Dict[str, float]:
    def filter_by_date(_t: Transaction) -> bool:
        try:
            dt = datetime.strptime(t["operation_date"], "%Y-%m-%d")
            return dt.year == year and dt.month == month
        except ValueError:
            logger.warning(f"Invalid date format in transaction: {t}")
            return False

    filtered = filter(filter_by_date, data)
    result: Dict[str, float] = {}

    for t in filtered:
        if t.get("cashback", 0) > 0:
            result[t["category"]] = result.get(t["category"], 0) + t["cashback"]

    return dict(sorted(result.items(), key=lambda x: -x[1]))


def investment_bank(month: str, transactions: List[Transaction], limit: int = 50) -> float:
    def is_target_month(t: Transaction) -> bool:
        return t["operation_date"].startswith(month)

    def calculate_rounding(t: Transaction) -> float:
        amount = abs(t["amount"])
        return (limit - (amount % limit)) % limit

    try:
        target_transactions = filter(is_target_month, transactions)
        roundings = map(calculate_rounding, target_transactions)
        return sum(roundings)
    except Exception as e:
        logger.error(f"Investment calculation failed: {str(e)}")
        raise


def simple_search(transactions: List[Transaction], query: str) -> List[Transaction]:
    def matches_query(t: Transaction) -> bool:
        return query.lower() in t["description"].lower() or query.lower() in t["category"].lower()

    try:
        return list(filter(matches_query, transactions))
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise


def find_phone_transactions(transactions: List[Transaction]) -> List[Transaction]:
    phone_pattern = re.compile(r"(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")

    def has_phone(t: Transaction) -> bool:
        return bool(phone_pattern.search(t["description"]))

    try:
        return list(filter(has_phone, transactions))
    except Exception as e:
        logger.error(f"Phone search failed: {str(e)}")
        raise


def find_person_transfers(transactions: List[Transaction]) -> List[Transaction]:
    name_pattern = re.compile(r"^[А-Я][а-я]+\s[А-Я]\.$")

    def is_person_transfer(t: Transaction) -> bool:
        return t["category"] == "Transfers" and bool(name_pattern.match(t["description"]))

    try:
        return list(filter(is_person_transfer, transactions))
    except Exception as e:
        logger.error(f"Person transfers search failed: {str(e)}")
        raise


def generate_excel_report(transactions: List[Dict], output_path: str, include_charts: bool = False) -> None:
    """
    Генерация Excel отчета с дополнительными возможностями

    Args:
        transactions: Список транзакций
        output_path: Путь для сохранения файла
        include_charts: Добавлять ли диаграммы в отчет
    """
    try:
        df = pd.DataFrame(transactions)

        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Transactions", index=False)

            if include_charts:
                workbook = writer.book
                worksheet = writer.sheets["Transactions"]

                # Добавление простой диаграммы
                chart = workbook.add_chart({"type": "column"})
                chart.add_series(
                    {
                        "values": "=Transactions!$B$2:$B$" + str(len(df) + 1),
                        "categories": "=Transactions!$D$2:$D$" + str(len(df) + 1),
                    }
                )
                worksheet.insert_chart("F2", chart)

    except Exception as e:
        logger.error(f"Excel report generation failed: {str(e)}")
        raise


def load_transactions_from_excel(file_path: str) -> List[Dict]:
    """Загрузка транзакций из Excel"""
    df = pd.read_excel(file_path)
    return df.to_dict("records")

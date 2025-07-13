from src.services import FinanceAnalyzer

def test_load_transactions():
    analyzer = FinanceAnalyzer()
    transactions = analyzer.load_transactions("data/operations.xlsx")
    assert len(transactions) > 0
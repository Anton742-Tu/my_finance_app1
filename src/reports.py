from xlsxwriter import Workbook

def generate_excel_report(transactions: list[dict], output_path: str):
    df = pd.DataFrame(transactions)
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Transactions', index=False)
        # Кастомное форматирование...
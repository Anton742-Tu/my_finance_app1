import pandas as pd
from typing import List
import os


def generate_excel_report(transactions: List[dict], output_path: str):
    """Генерация отчета с учетом реальной структуры данных"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Преобразуем в DataFrame
    data = [t.model_dump(by_alias=True) for t in transactions]
    df = pd.DataFrame(data)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Транзакции', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Транзакции']

        # Форматирование
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'dd.mm.yyyy hh:mm'})

        # Применяем форматы
        worksheet.set_column('A:B', 20, date_format)
        money_cols = ['E', 'G', 'I', 'L', 'M', 'N']
        for col in money_cols:
            worksheet.set_column(f'{col}:{col}', 15, money_format)

        # Добавляем сводную таблицу
        if len(df) > 0:
            pivot_table = df.pivot_table(
                index='Категория',
                values='Сумма операции',
                aggfunc='sum'
            ).reset_index()

            pivot_table.to_excel(
                writer,
                sheet_name='Сводка',
                index=False,
                startrow=3
            )

            # Форматирование сводки
            pivot_sheet = writer.sheets['Сводка']
            pivot_sheet.write(0, 0, "Итого потрачено:")
            total_formula = f"=SUM(C4:C{len(pivot_table) + 3})"
            pivot_sheet.write_formula(0, 1, total_formula, money_format)
from src.utils.parsers import parse_excel_to_db

if __name__ == "__main__":
    parse_excel_to_db("data/operations.xlsx")
    print("Данные успешно загружены в БД!")
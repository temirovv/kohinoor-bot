import openpyxl
from data.config import EXCEL_FILE


def convert_to_excel(data: list) -> list:
    all_in_list = [
        ["Full name", " Telefon raqami", "Nechta odam taklif qilgan", "Telegram Aydisi"]
    ]
    for full_name, phone_number, people_invited, telegram_id in data:
        all_in_list.append(
            [full_name, phone_number, people_invited, telegram_id]
        )

    return all_in_list


def save_to_excel(data: list):
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "MyData"

    for row in data:
        sheet.append(row)

    workbook.save(EXCEL_FILE)
    return "success"



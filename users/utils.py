from openpyxl import load_workbook
from users.models import User
import re


def create_users_from_excel_file(file):
    error = None

    data = extract_excel_data(file)

    if not data[0] == ["email", "first_name", "last_name", "team"]:
        error = "Please make sure to use the right header order: | email | first_name | last_name | team |"
        return None, error

    headers = data.pop(0)
    new_users = 0
    existing_users = 0
    invalid_users = 0

    for user in data:
        if not _is_valid_email(user[0]):
            invalid_users += 1
            user.append("not a correct email")
            continue

        created = create_user(user)
        if not created:
            existing_users += 1
            user.append("user already exists")
        else:
            new_users += 1
            user.append("user created")

    data.insert(0, headers)
    data.insert(
        0,
        [
            f"{new_users} new user(s) are created",
            f"{existing_users} user(s) where already present",
            f"{invalid_users} invalid email(s)",
        ],
    )

    return data, None


def extract_excel_data(file):
    # Return extracted excel data

    wb = load_workbook(file)

    worksheet = wb.worksheets[0]
    return [[cell.value for cell in row] for row in worksheet.rows]


def create_user(user_data):
    # create users from the extracted excel data
    if not user_data[0]:
        return False

    user, created = User.objects.get_or_create(email=user_data[0])

    if not created:
        return False

    user.first_name = user_data[1]
    user.last_name = user_data[2]
    user.username = user_data[1] + "" + user_data[2]
    user.team = user_data[3]

    user.save()

    return True


def _is_valid_email(email):
    # Regular expression for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if not re.fullmatch(regex, email):
        return False

    return True

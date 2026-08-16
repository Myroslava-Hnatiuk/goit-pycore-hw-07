from datetime import datetime, timedelta

def get_congratulations_date(birthday: datetime) -> datetime:
    if birthday.weekday() == 5:  # Saturday
        return birthday + timedelta(days=2) # If the birthday falls on a Saturday, the congratulations date is set to the following Monday (2 days later).
    if birthday.weekday() == 6:  # Sunday
        return birthday + timedelta(days=1) # If the birthday falls on a Sunday, the congratulations date is set to the following Monday (1 day later).
    return birthday


def build_birthday_record(user: dict[str, str], birthday: datetime) -> dict[str, str]:
    congratulation_date = get_congratulations_date(birthday)
    return {
        "name": user.name.value,
        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
    }

def get_upcoming_birthdays(users: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    today = datetime.today().date() # Get today's date as a date object
    upcoming_birthdays = [] # List to store users with upcoming birthdays

    for user in users.values(): # Iterate through each user in the dictionary
        if user.birthday is None: # Skip users without a birthday
            continue
        birthday = user.birthday.value  # .value contains the datetime object
        birthday_this_year = datetime(
            today.year,
            birthday.month,
            birthday.day
        ).date()
       
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        date_diff = (birthday_this_year - today).days # Calculate the difference in days between the birthday and today
        if 0 <= date_diff <= 7: # Include birthdays from today through the next 7 days inclusive
            upcoming_birthdays.append(build_birthday_record(user, birthday_this_year))

    return upcoming_birthdays
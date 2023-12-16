import pandas as pd
from datetime import datetime

def load_data() -> pd.DataFrame:
    print("Loading data...")
    messages = pd.read_json("messages.json")
    messages["date"] = pd.to_datetime(messages["date"], format="%d/%m/%y, %H:%M")

    return messages


def get_messages_in_year(year: int = datetime.now().year) -> pd.DataFrame:
    messages = load_data()
    messages_2023 = messages[messages["date"].dt.year == year]

    return messages_2023


def count_messages_per_sender(messages: pd.DataFrame) -> pd.DataFrame:
    messages_per_sender = messages.groupby("sender").count()["message"].reset_index()
    return messages_per_sender


def count_messages_per_receiver(messages: pd.DataFrame) -> pd.DataFrame:
    messages_per_receiver = (
        messages.groupby("receiver").count()["message"].reset_index()
    )
    columns = ["receiver", "messages"]
    messages_per_receiver.columns = columns
    return messages_per_receiver


def count_messages_per_day(messages: pd.DataFrame) -> pd.DataFrame:
    messages_per_day = (
        messages.groupby(messages["date"].dt.date).count()["message"].reset_index()
    )
    messages_per_day.columns = ["date", "messages"]
    return messages_per_day

def count_messages_per_week_day(messages: pd.DataFrame) -> pd.DataFrame:
    messages_per_week_day = (
        messages.groupby(messages["date"].dt.day_name()).count()["message"].reset_index()
    )
    messages_per_week_day.columns = ["week_day", "messages"]
    return messages_per_week_day

def count_messages_per_month(messages: pd.DataFrame) -> pd.DataFrame:
    messages_per_month = (
        messages.groupby(messages["date"].dt.month).count()["message"].reset_index()
    )
    messages_per_month.columns = ["month", "messages"]

    return messages_per_month


def messages_per_contact(messages: pd.DataFrame) -> pd.DataFrame:
    sent_messages = count_messages_per_sender(messages)
    received_messages = count_messages_per_receiver(messages)

    messages_per_contact = pd.merge(
        sent_messages,
        received_messages,
        left_on="sender",
        right_on="receiver",
        how="outer",
        validate="one_to_one",
    )

    messages_per_contact["Person"] = messages_per_contact["sender"].combine_first(
        messages_per_contact["receiver"]
    )
    messages_per_contact = messages_per_contact.drop(["sender", "receiver"], axis=1)

    messages_per_contact.columns = ["sent_messages", "received_messages", "person"]

    messages_per_contact["received_messages"] = (
        messages_per_contact["received_messages"].fillna(0).astype(int)
    )
    messages_per_contact["sent_messages"] = (
        messages_per_contact["sent_messages"].fillna(0).astype(int)
    )

    messages_per_contact["total_messages"] = (
        messages_per_contact["sent_messages"]
        + messages_per_contact["received_messages"]
    )

    messages_per_contact = messages_per_contact[
        ["person", "sent_messages", "received_messages", "total_messages"]
    ]

    return messages_per_contact


def get_year_days_without_message(messages_per_day: pd.DataFrame, year: int) -> pd.DatetimeIndex:
    days = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31")
    days_without_message = days[~days.isin(messages_per_day.date)]

    return days_without_message


def get_top_x_persons(
    messages_per_contact: pd.DataFrame, column_name: str, x: int
) -> pd.DataFrame:
    print(f"Getting top {x} persons...")
    sorted_val = (
        messages_per_contact[messages_per_contact["person"] != "Me"]
        .sort_values(column_name, ascending=False)
        .head(x)
    )

    top_x_persons = sorted_val[["person", column_name]]
    return top_x_persons


def number_of_sent_by_me(messages_per_sender: pd.DataFrame) -> int:
    return messages_per_sender[messages_per_sender["sender"] == "Me"]["message"].values[
        0
    ]

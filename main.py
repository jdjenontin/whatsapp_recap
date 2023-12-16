from datetime import datetime

import typer
from typing_extensions import Annotated

import analyze
from reporter import Reporter
import etl

def main(path: Annotated[str, typer.Option(help="The path to the chats folder")] = "chats", 
         year: Annotated[int, typer.Option(help="The year to analyze")] = datetime.now().year, 
         number_of_top_persons: Annotated[int, typer.Option(help="The number of top persons for each category")] = 10
         ):
    
    print("Extracting...")
    etl.etl(path)

    year_messages = analyze.get_messages_in_year(year)

    print("Analysing...")

    messages_per_sender = analyze.count_messages_per_sender(year_messages)

    messages_per_day = analyze.count_messages_per_day(year_messages)
    messages_per_month = analyze.count_messages_per_month(year_messages)
    messages_per_contact = analyze.messages_per_contact(year_messages)
    days_without_message = analyze.get_year_days_without_message(messages_per_day, year)

    print("Exporting...")
    messages_per_day.to_csv("messages_per_day.csv", index=False)
    messages_per_month.to_csv("messages_per_month.csv", index=False)
    messages_per_contact.to_csv("messages_per_contact.csv", index=False)


    # Report
    total_messages = len(year_messages)
    sent_by_me = analyze.number_of_sent_by_me(messages_per_sender)

    report_data = {
        "YEAR": year,
        "n": number_of_top_persons,
        "total_messages": total_messages,
        "nb_discussion": len(messages_per_contact),
        "nb_day_without_message": len(days_without_message),
        "nb_sent": sent_by_me,
        "nb_received": total_messages - sent_by_me,
        "top_senders": analyze.get_top_x_persons(messages_per_contact, "sent_messages", number_of_top_persons).to_dict(orient="records"),
        "top_receivers": analyze.get_top_x_persons(messages_per_contact, "received_messages", number_of_top_persons).to_dict(orient="records"),
        "top_contacts": analyze.get_top_x_persons(messages_per_contact, "total_messages", number_of_top_persons).to_dict(orient="records"),
    }
    

    Reporter(report_data).generate()

    print("Done!")


if __name__ == "__main__":
    typer.run(main)

# WhatsApp Recap

This is a simple CLI project to analyze WhatsApp data for a specific year. Please note that this version does not support group messages.

## Requirements
- The project has been developed using Python 3.11.
- The dependent libraries are listed in `requirements.txt`.

## Data

The data used by the project are exported from WhatsApp. The procedure for exporting can be found [here](https://faq.whatsapp.com/1180414079177245/?locale=en_US&cms_platform=android&cms_id=1180414079177245&draft=false): **Export chat**.

**NB:** Unfortunately, WhatsApp does not have a bulk export option. Some third-party apps offer that possibility, but I won't recommend any here due to privacy concerns.

The exported data should be placed in the `chats` folder at the root of the project.

## Usage

The project uses [Typer](https://typer.tiangolo.com/) for the CLI. It takes three optional options and one mandatory argument:

```bash
python main.py [OPTION] NAME
```

- `NAME`  Your WhatsApp name, as it appears in the chat files
`--path`: The path to the chats folder, defaulting to chats.
- `--year`: The year to analyze, defaulting to the current year.
- `--number-of-top-persons`: The number of top persons for each category, defaulting to 10.

Example 

```bash
python main.py --year 2021 --path Chats --number-of-top-persons 12 "jdjenontin"
```

The program generates five files:

- `messages.json` with every message in the folder.
- `messages_per_contact.csv` with the number of messages sent to and received from every contact.
- `messages_per_day.csv` with the number of messages sent and received per day.
- `messages_per_month.csv` with the number of messages sent and received per month.
- `report.txt`: A report with some key information like top senders, receivers, and contacts.

## Warning

Depending on how your contacts are named, some issues can occur.
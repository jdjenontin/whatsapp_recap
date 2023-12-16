from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


class Reporter:
    def __init__(self, data: dict):
        self.data = data

    def generate(self):
        print("Generating report...")
        template = env.get_template("report_template.txt")
        rendered = template.render(self.data)

        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(rendered)

import csv
from faker import Faker
import datetime


def datagenerate(records, headers):
    fake = Faker('fr_FR')
    with open("interv.csv", 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            writer.writerow({
                "patient": i,
                "IntervDate": fake.date_between(start_date=datetime.date(2022, 8, 1),
                                                end_date=datetime.date(2022, 9, 6)),
                "Dh": fake.random_int(min=75, max=500),
                "uuid": fake.uuid4(),
            })


if __name__ == '__main__':
    records = 1000
    headers = ["patient", "IntervDate", "Dh", "uuid"]
    datagenerate(records, headers)

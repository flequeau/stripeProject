import csv
from faker import Faker
import datetime


def datagenerate(records, headers):
    fake = Faker('fr_FR')
    with open("patients.csv", 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]

            writer.writerow({
                "Name": Lname,
                "Forname": Fname,
                "BirthDate": fake.date(pattern="%Y-%m-%d", end_datetime=datetime.date(2000, 1, 1)),
                "PhoneNumber": fake.phone_number().replace("+33", "-").replace(" ", "").replace("(", "").replace(")",
                                                                                                                 "")
                .replace("-", "0"),
                "Email": fake.email(),
                "Address": fake.address(),
            })


if __name__ == '__main__':
    records = 1000
    headers = ["Name", "Forname", "BirthDate", "PhoneNumber", "Email",
               "Address"]
    datagenerate(records, headers)

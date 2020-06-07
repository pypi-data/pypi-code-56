import csv
from models.Address import Address

data = []
with open('bad.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    next(reader)  # Скип первой строчки
    for row in reader:
        addr = Address(row[1])
        data.append([row[0], row[1], addr.address_string()])


with open('fixed_bad.csv', 'w', encoding="utf-8", newline='') as csvfile:
    fieldnames = ['id', 'address', "normalized_address"]
    writer = csv.writer(csvfile, delimiter=';', quotechar='"')
    writer.writerow(fieldnames)
    for i in data:
        writer.writerow(i)

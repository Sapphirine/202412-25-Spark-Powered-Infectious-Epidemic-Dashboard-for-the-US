import pandas as pd
import csv


# .csv->.txt
def transfer_csv():
    data = pd.read_csv('./data/us-counties-max.csv')
    with open('./data/us-counties-max.txt', 'a+', encoding='utf-8') as f:
        for line in data.values:
            f.write((str(line[0]) + '\t' + str(line[1]) + '\t'
                     + str(line[2]) + '\t' + str(line[3]) + '\t' + str(line[4]) + '\n'))


def transfer_date():
    input_csv = "us-counties-max.csv"
    output_txt = "us-counties-max.txt"

    with open(input_csv, "r") as csv_file, open(output_txt, "w") as txt_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)

        for row in csv_reader:
            # delete 'fips'
            del row[3]
            txt_file.write("\t".join(row) + "\n")

    print(f"result saved as {output_txt}")


transfer_date()

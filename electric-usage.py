import argparse
import csv
from dateutil import parser as date_parser
from pytz import timezone
import os

my_timezone = timezone('US/Pacific')


def main(csv_file):
    f_in = open(csv_file, 'r')
    reader = csv.reader(f_in)
    headers = next(reader, None)

    column = {}
    for h in headers:
        column[h] = []

    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)

    utc_hdr = headers[0]
    utc_col = column[utc_hdr]

    pst_col = ['PST']

    for utc in utc_col:
        date = date_parser.parse(utc)
        date = my_timezone.localize(date)
        date = date.astimezone(my_timezone)
        pst_col.append(date)

    x = os.path.splitext(csv_file)
    csv_file_new = f'{x[0]}-PST{x[1]}'
    with open(csv_file_new, '+w', newline='') as f:
        writer = csv.writer(f)
        f_in.seek(0)
        i = 0
        for row in reader:
            if i == 0:
                row[0] = pst_col[i]
            else:
                row[0] = pst_col[i].strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(row)
            i += 1

    print('done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process electric usage.')
    parser.add_argument('-c', '--csv', required=True, help='CSV file to parse')

    args = parser.parse_args()
    main(args.csv)

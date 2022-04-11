import argparse
import csv
from dateutil import parser as date_parser
from pytz import timezone
import os

PST = timezone('US/Pacific')

COL_TIMESTAMP = 0


def main(csv_file):
    f_in = open(csv_file, 'r')
    reader = csv.reader(f_in)

    headers = next(reader, None)
    rows = []

    for row in reader:
        rows.append(row)

    x = os.path.splitext(csv_file)
    csv_file_new = f'{x[0]}-SUMMARY{x[1]}'
    with open(csv_file_new, '+w', newline='') as f:
        writer = csv.writer(f)
        headers[0] = 'Month'
        writer.writerow(headers)

        month = None
        sums = None

        for row in rows:
            date = date_parser.parse(row[COL_TIMESTAMP])
            date = PST.localize(date)
            pst = date.astimezone(PST)

            if month is not None and pst.month != month:
                # todo: print sums
                writer.writerow(sums)
                month = None

            if month is None:
                month = pst.month
                sums = [0] * len(row)
                sums[0] = month

            for i in range(1, len(row)):
                sums[i] += float(row[i])

        writer.writerow(sums)
    print('done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process electric usage.')
    parser.add_argument('-c', '--csv', required=True, help='CSV file to parse')

    args = parser.parse_args()
    main(args.csv)

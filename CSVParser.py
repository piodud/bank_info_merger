import csv
from datetime import datetime

from TransactionInfo import TransactionInfo


def translate_timestamp(timestamp: str, date_format: str):
    return datetime.strptime(timestamp, date_format).strftime(TransactionInfo.UNIFIED_DATE_FORMAT)


def translate_to_amount(euro: str, cents: str):
    return '.'.join([euro, cents])


def map_format_1(row):
    timestamp = translate_timestamp(row['timestamp'], date_format='%b %d %Y')

    return TransactionInfo(
        timestamp=timestamp,
        transaction_type=row['type'],
        amount=row['amount'],
        sent_from=row['from'],
        sent_to=row['to']
    )


def map_format_2(row):
    return TransactionInfo(
        timestamp=row['date'],
        transaction_type=row['transaction'],
        amount=row['amounts'],
        sent_from=row['from'],
        sent_to=row['to']
    )


def map_format_3(row):
    timestamp = translate_timestamp(row['date_readable'], date_format='%d %b %Y')
    amount = translate_to_amount(row['euro'], row['cents'])
    return TransactionInfo(
        timestamp=timestamp,
        transaction_type=row['type'],
        amount=amount,
        sent_from=row['from'],
        sent_to=row['to']
    )


class CSVParser:
    HEADERS_MAPPER = {
        ('timestamp', 'type', 'amount', 'from', 'to'): map_format_1,
        ('date', 'transaction', 'amounts', 'to', 'from'): map_format_2,
        ('date_readable', 'type', 'euro', 'cents', 'to', 'from'): map_format_3,
    }

    def parse(self, file_path: str):
        transaction_info_list = list()
        with open(file_path) as file:
            print(f'Parsing {file_path}')
            reader = csv.DictReader(file)
            if reader.fieldnames:
                mapper = self.HEADERS_MAPPER[tuple(reader.fieldnames)]
                for row in reader:
                    transaction_info_list.append(mapper(row).to_list())
                print(transaction_info_list)
                return transaction_info_list

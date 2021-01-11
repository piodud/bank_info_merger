import csv
import os
from pathlib import Path

from CSVParser import CSVParser
from TransactionInfo import TransactionInfo


def main():
    app = Merger()
    app.run()
    return 0


class Merger:

    def __init__(self):
        self.unified_data = list()
        self._csv_parser = CSVParser()
        # self._json_parser = JSONParser()
        # self._xml_parser = JSONParser()
        self.extension_map = {
            ".csv": self._csv_parser,
            # ".json": self._json_parser,
            # ".json": self._xml_parser,
        }

    def run(self, sources_dir: str = 'source_files/'):
        for file in os.listdir(sources_dir):
            in_file = Path(sources_dir, file)
            parser = self._match_parser_to_extension(in_file)
            if parser is not None:
                parsed_data = parser.parse(in_file)
                if parsed_data:
                    self.unified_data.extend(parsed_data)
        print(self.unified_data)
        self.save_to_csv()

    def _match_parser_to_extension(self, input_file_path):
        extension = input_file_path.suffix
        if extension not in self.extension_map.keys():
            print("Unknown extension for file in {}".format(input_file_path))
            return None
        return self.extension_map[extension]

    def save_to_csv(self):
        with open("out.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(TransactionInfo.__slots__)
            writer.writerows(self.unified_data)


if __name__ == "__main__":
    main()

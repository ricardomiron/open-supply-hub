from typing import List
from contricleaner.lib.parsing_strategies.abstractions.strategy import (
    ParsingStrategy
    )
from contricleaner.lib.parsers.parsing_executor import (
    ParsingExecutor
)
from contricleaner.lib.parsers.csv_parser import (
    CSVParser
)


# List Upload Parsing Strategy
class CSVParsingStrategy(ParsingStrategy):
    def define_parsing_strategy(self, data: List[dict]):
        return ParsingExecutor(
                    CSVParser(data)
                )

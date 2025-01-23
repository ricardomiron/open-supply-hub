from typing import List
from contricleaner.lib.parsing_strategies.abstractions.parsing_strategy import (ParsingStrategy)
from contricleaner.lib.parsers.parsing_executor import (
    ParsingExecutor
)
from contricleaner.lib.parsers.xlsx_parser import (
    XLSXParser
)


# List Upload Parsing Strategy
class XLSXParsingStrategy(ParsingStrategy):
    def define_parsing_strategy(self, data: List[dict]):
        return ParsingExecutor(
                    XLSXParser(data)
                )

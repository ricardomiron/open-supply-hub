from contricleaner.lib.parsing_strategies.abstractions.strategy import (
    ParsingStrategy
)
from contricleaner.lib.parsers.parsing_executor import (
    ParsingExecutor
)
from contricleaner.lib.parsers.json_parser import (
    JSONParser
)


# API Upload Parsing Strategy
class JSONParsingStrategy(ParsingStrategy):
    def define_parsing_strategy(self, data: dict):
        return ParsingExecutor(
                    JSONParser(data)
                )

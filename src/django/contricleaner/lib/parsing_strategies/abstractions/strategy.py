from contricleaner.lib.parsers.parsing_executor import (
    ParsingExecutor
)
from abc import ABC, abstractmethod


class ParsingStrategy(ABC):
    @abstractmethod
    def define_parsing_strategy(self, data) -> ParsingExecutor:
        pass

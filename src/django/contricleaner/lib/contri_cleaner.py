import os
from typing import Union, List, Dict

from django.core.files.base import File

from contricleaner.lib.client_abstractions.sector_cache_interface import (
    SectorCacheInterface
)
from contricleaner.lib.parsing_strategies.json_parsing_strategy import (
    JSONParsingStrategy
)
from contricleaner.lib.parsing_strategies.xlsx_parsing_strategy import (
    XLSXParsingStrategy
)
from contricleaner.lib.parsing_strategies.csv_parsing_strategy import (
    CSVParsingStrategy
)
from contricleaner.lib.dto.list_dto import ListDTO
from contricleaner.lib.exceptions.parsing_error import ParsingError
from contricleaner.lib.handlers.list_row_handler import ListRowHandler
from contricleaner.lib.handlers.pre_validation_handler \
    import PreValidationHandler
from contricleaner.lib.handlers.serialization_handler \
    import SerializationHandler
from contricleaner.constants import (
  NON_FIELD_ERRORS_KEY, OperationType, FileExtension, FILE_EXTENSION_ERROR)


class ContriCleaner:
    '''
    This is the facade for interacting with the ContriCleaner library.
    '''

    def __init__(self,
                 data: Union[File, Dict],
                 sector_cache: SectorCacheInterface) -> None:
        unsupported_data_value_type_message = ('The data value type should be '
                                               'either dict or File.')
        unsupported_sector_cache_value_type_message = (
            'The sector_cache value type should be SectorCacheInterface.')
        assert isinstance(
            data,
            (dict, File)
        ), unsupported_data_value_type_message
        assert isinstance(
            sector_cache, SectorCacheInterface
        ), unsupported_sector_cache_value_type_message

        self.__data = data
        self.__sector_cache = sector_cache

        self.strategies = {
            "api_post_facilities": JSONParsingStrategy(),
            "api_post_patch_production_location": JSONParsingStrategy(),
            "file_xlsx": XLSXParsingStrategy(),
            "file_csv": CSVParsingStrategy()
        }

    def process_data(self, source_type, operation_type) -> ListDTO:
        self.source_type = source_type
        self.operation_type = operation_type

        try:
            parsed_rows = self.__parse_data()
        except ParsingError as err:
            return ListDTO(errors=[{
                'message': str(err),
                'field': NON_FIELD_ERRORS_KEY,
                'type': 'ParsingError',
            }])

        entry_handler = self.__setup_handlers()

        processed_list = entry_handler.handle(parsed_rows)

        return processed_list

    def __parse_data(self) -> List[Dict]:
        parsing_executor = self.__define_parsing_strategy()
        parsed_rows = parsing_executor.execute_parsing()

        return parsed_rows

    def __define_parsing_strategy(self):
        """
        source_type: "api" (API Upload) or "file" (List Upload)
        operation_type: "post_facilities", "post_patch_production_location",
          "xlsx", "csv"
        """
        if self.operation_type == '':
            raise ParsingError(f"{FILE_EXTENSION_ERROR}")
        strategy_key = f"{self.source_type}_{self.operation_type}"
        strategy = self.strategies.get(strategy_key)
        if not strategy:
            raise ParsingError(f"No parsing strategy for: {strategy_key}")

        return strategy.define_parsing_strategy(self.__data)

    def __setup_handlers(self) -> ListRowHandler:
        handlers = (
            PreValidationHandler(),
            SerializationHandler(self.__sector_cache)
        )
        for index in range(len(handlers) - 1):
            handlers[index].set_next(handlers[index + 1])

        entry_handler = handlers[0]

        return entry_handler

    def get_operation_type_for_file(self) -> str:
        """Get operation type based on file extension"""
        file_extension = os.path.splitext(self.__data.name)[1].lower()

        if file_extension not in {FileExtension.CSV, FileExtension.XLSX}:
            return ''

        operation_type = (
            OperationType.XLSX
            if file_extension == FileExtension.XLSX
            else OperationType.CSV
        )

        return operation_type

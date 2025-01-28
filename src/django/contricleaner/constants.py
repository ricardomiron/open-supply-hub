MAX_PRODUCT_TYPE_COUNT = 50
DEFAULT_SECTOR_NAME = 'Unspecified'

# Validation errors will include field names as keys in the response. If the
# error isn’t field-specific, ContriCleaner will use the non_field_errors key
# for issues spanning multiple fields or related to the overall data object.
NON_FIELD_ERRORS_KEY = 'non_field_errors'


class SourceType:
    API = 'api'
    FILE = 'file'


class OperationType:
    FACILITIES = "post_facilities"
    PRODUCTION_LOCATION = "post_patch_production_location"
    XLSX = "xlsx"
    CSV = "csv"


class FileExtension:
    CSV = '.csv'
    XLSX = '.xlsx'


FILE_EXTENSION_ERROR = 'We cannot accept the type of file you submitted.\
      Please change your file to an Excel or UTF-8 CSV and reupload.'

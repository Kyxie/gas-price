import re


class Constants:
    # url
    TARGET = "https://gaswizard.ca/"

    # Patterns
    START_PATTERN = r'class="single-city-prices"'
    DAY_PATTERN = r"Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
    DATE_PATTERN = (
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}"
    )
    REGU_PATTERN = r"Regular<\/div><div class=\"fuelprice\">(\d{3}\.\d)\s*\(<span class=\"price-direction (?:pd-nc|pd-up|pd-down)\">(\+?\-?\d*¢|n\/c)<\/span>\)"
    PREM_PATTERN = r"Premium<\/div><div class=\"fuelprice\">(\d{3}\.\d)\s*\(<span class=\"price-direction (?:pd-nc|pd-up|pd-down)\">(\+?\-?\d*¢|n\/c)<\/span>\)"

    # Pattern mode
    LINE = 1  # 1 means return the whole line
    MATCH = 2  # 2 means only return matched part
    ALL = 3  # 3 means find all the matched parts

    # Output file
    TXT_FILE = "./gas_price.txt"

    @staticmethod
    def pattern_parser(pattern, text, mode):
        if mode == Constants.ALL:
            return re.findall(pattern, text) or []

        match = re.search(pattern, text)
        if not match:
            return None

        if mode == Constants.LINE:
            return text
        elif mode == Constants.MATCH:
            return match.group()

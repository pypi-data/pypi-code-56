from bibchex.config import Config
from bibchex.util import parse_datetime, contains_abbreviation
from bibchex.checks.common import GenericFuzzySimilarityChecker,\
    GenericAbbrevChecker


class JournalAbbrevChecker(object):
    NAME = 'journal-abbrev'
    FIELDS = ['booktitle', 'journal']

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        if not self._cfg.get('journal_no_abbrevs', entry, True):
            return []

        problems = []
        for field in JournalAbbrevChecker.FIELDS:
            val = entry.data.get(field, '')
            if contains_abbreviation(val):
                problems.append(
                    ("abbreviated_journal",
                     "Publication title '{}' seems to contain an abbreviation"
                     .format(val), ""))

        return problems


class JournalSimilarityChecker(GenericFuzzySimilarityChecker):
    NAME = 'journal_similarity'
    FIELDS = ['booktitle', 'journal']
    MSG_NAME = "Journal"


class PublisherSimilarityChecker(GenericFuzzySimilarityChecker):
    NAME = 'publisher_similarity'
    FIELDS = ['organization', 'publisher']
    MSG_NAME = "Publisher"


class JournalMutualAbbrevChecker(GenericAbbrevChecker):
    NAME = 'journal_mutual_abbrev'
    MSG_NAME = 'Journal'
    FIELDS = ['booktitle', 'journal']


class PublisherMutualAbbrevChecker(GenericAbbrevChecker):
    NAME = 'publisher_mutual_abbrev'
    MSG_NAME = 'Publisher'
    FIELDS = ['organization', 'publisher']


class PreferOrganizationChecker(object):
    NAME = 'prefer-organization'

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        if not self._cfg.get('prefer_organization', entry, True):
            return []

        if entry.data.get('publisher') and not entry.data.get('organization'):
            return [("prefer_organization",
                     "Entry should prefer organization over publisher.", "")]
        else:
            return []


class PreferDateChecker(object):
    NAME = 'prefer-date'

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        if not (self._cfg.get('prefer_date', entry, False) or
                self._cfg.get('prefer_date_or_year', entry, True)):
            return []

        if (any((entry.data.get(key) for key in ('year', 'month', 'day'))) and
            self._cfg.get('prefer_date', entry, False) or
                (any((entry.data.get(key) for key in ('month', 'day'))) and
                 self._cfg.get('prefer_date_or_year', entry, True))) and \
                not entry.data.get('date'):
            return [('prefer_date',
                     ("The 'date' field is preferred over "
                      "the 'day/month/year' fields."),
                     "")]

        return []


class DateParseableChecker(object):
    NAME = 'date-parseable'

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        if not self._cfg.get('parseable_date', entry, True):
            return []

        if not entry.data.get('date'):
            return []

        try:
            d = parse_datetime(entry.data.get('date'))
            print(d)
            return []
        except ValueError:
            return [('date_parseable',
                     "Unparseable date",
                     "The date string '{}' could not be parsed."
                     .format(entry.data.get('date')))]

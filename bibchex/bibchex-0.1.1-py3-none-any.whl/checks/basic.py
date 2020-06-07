import aiohttp
import re

from bibchex.config import Config


class DOIChecker(object):
    NAME = "doi"

    def __init__(self):
        pass

    async def check(self, entry):
        doi = entry.data.get('doi')
        if not doi:
            suggested_doi = entry.get_doi()
            details = ""
            if suggested_doi:
                details = "Suggested DOI: {}".format(suggested_doi)
            elif entry.get_suggested_dois():
                details = "Suggested DOIs: {}".format(
                    entry.get_suggested_dois())

            return [("missing_doi", "Missing DOI", details)]
        else:
            return []


class URLChecker(object):
    NAME = "url"
    DOI_RE = re.compile(r'https?://(dx\.)?doi.org/.*')
    HTTP_RE = re.compile(r'https?://.*', re.IGNORECASE)

    async def check(self, entry):
        url = entry.data.get('url')
        problems = []
        if not url:
            return []

        m = URLChecker.DOI_RE.match(url)
        if m:
            problems.append(("doi_url", "URL points to doi.org", ""))

        m = URLChecker.HTTP_RE.match(url)
        if not m:
            # Not a http / https URL. We don't know how to handle this.
            return problems

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status = resp.status
                if status >= 400 or status < 200:
                    problems.append(("dead_url", "URL seems inaccessible",
                                     "Accessing URL '{}' gives status code {}"
                                     .format(url, status)))

        return problems


class RequiredFieldsChecker(object):
    NAME = "required_fields"

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        problems = []

        required_fields = self._cfg.get('required', entry)
        for field_raw in required_fields:
            field = field_raw.lower()

            if field == 'author':
                # Special handling
                if len(entry.authors) == 0:
                    problems.append(
                        ("missing_field",
                         "Required field 'author' missing", ""))
            elif field == 'editor':
                # Special handling
                if len(entry.editors) == 0:
                    problems.append(
                        ("missing_field",
                         "Required field 'editor' missing", ""))
            else:
                if field not in entry.data:
                    problems.append(
                        ("missing_field",
                         "Required field '{}' missing".format(field), ""))

        return problems


class ForbiddenFieldsChecker(object):
    NAME = "forbidden_fields"

    def __init__(self):
        self._cfg = Config()

    async def check(self, entry):
        problems = []

        forbidden_fields = self._cfg.get('forbidden_fields', entry, [])
        for field_raw in forbidden_fields:
            field = field_raw.lower()

            if field == 'author':
                # Special handling
                if len(entry.authors) >= 0:
                    problems.append(
                        ("forbidden_field",
                         "Forbidden field 'author' present", ""))
            if field == 'editor':
                # Special handling
                if len(entry.editors) >= 0:
                    problems.append(
                        ("forbidden_field",
                         "Forbidden field 'editor' present", ""))
            else:
                if field in entry.data:
                    problems.append(
                        ("forbidden_field",
                         "Forbidden field '{}' present".format(field), ""))

        return problems

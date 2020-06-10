from typing import List

import httpx

from .model import Word


class MWClient:
    def __init__(self, key: str) -> None:
        self.key = key

    def get(self, word: str) -> Word:
        r = httpx.get(
            f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={self.key}"
        )    
        r_json = self._get_response_json(r)
        return [Word.from_response(w) for w in r_json]

    async def aget(self, word: str) -> Word:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={self.key}"
            )
        r_json = self._get_response_json(r)
        return [Word.from_response(w) for w in r_json]

    def _get_response_json(self, response: httpx.Response) -> List[dict]:
        if response.status_code != 200:
            raise AttributeError(
                f"API returned response with status code {response.status_code}."
            )
        r = response.json()
        if not r:
            raise ValueError("API returned empty response. Verify that the word is spelled correctly.")
        elif all(isinstance(i, str) for i in r):
            suggestions = ", ".join([f"'{s}'" for s in r])
            raise ValueError(f"Unable to find definition, did you mean: {suggestions}?")
        return r


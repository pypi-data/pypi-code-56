"""
Author: barbacbd
Date:   5/16/2020
"""
from nautical.io.web import get_noaa_forecast_url, get_url_source
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.noaa.buoy.buoy import Buoy
from bs4 import BeautifulSoup
from re import sub


# Default text to use as a search parameter for obtaining buoy
# information from a table
_DEFAULT_BUOY_WAVE_TEXT_SEARCH = "Conditions at {} as of"

# Default text to use as a search parameter for obtaining swell
# information from a table
_SWELL_DATA_TEXT_SEARCH = "Detailed Wave Summary"

# Text to search for previous observations. These values
# may occur in multiple tables. Unfortunately we have to
# provide exact text matches
_PREVIOUS_OBSERVATION_SEARCH = "Previous observations"


def create_buoy(buoy):
    """
    Provide a full workup for a specific buoy. If the buoy is None or it cannot be found
    then the data returned will be considered invalid as None
    :param buoy: id of the buoy to do a workup on
    :return: BuoyWorkup if successful else None
    """
    if buoy is not None:
        url = get_noaa_forecast_url(buoy)
        soup = get_url_source(url)

        current_buoy_data = BuoyData()
        get_current_data(soup, current_buoy_data, _DEFAULT_BUOY_WAVE_TEXT_SEARCH.format(buoy))
        get_current_data(soup, current_buoy_data, _SWELL_DATA_TEXT_SEARCH)
        past_data = get_past_data(soup)

        buoy_data = Buoy(buoy)
        buoy_data.present = current_buoy_data
        buoy_data.past = past_data

        return buoy_data

    else:
        return None


def get_current_data(soup: BeautifulSoup, buoy: BuoyData, search: str):
    """
    Search the beautiful soup object for a TABLE containing the search string. The function will
    grab the data from the table and create a NOAAData object and return the data
    :param soup: beautiful soup object generated from the get_url_source()
    :param buoy: BuoyData object that should be filled with data as this function parses the data.
    :param search: text to search for in the soup object. The text MUST be an exact match as this is
                   a possible limitation of beautiful soup searching
    """
    table = soup.find(text=search).findParent("table")

    for i, row in enumerate(table.findAll('tr')):

        # the first table is another table and it is no use to use -- skipping
        if i >= 1:
            cells = row.findAll('td')

            if cells:

                key_data = cells[1].next.split()
                key = sub('[():]', '', key_data[len(key_data) - 1]).lower()
                value = cells[2].next.split()[0]

                buoy.set(key, value)


def get_past_data(soup: BeautifulSoup):
    """
    Find all Previous Observations or Past Data.
    :param soup: beautiful soup object generated from the get_url_source()
    :return: list of all previous observations from the url. The buoy data returned in the list
             may be a comprehension of swell and wave data.
    """

    past_data = {}

    # Get a list of all tables of the type dataTable, we know that is what
    # type of xml tag we need information from
    tables = soup.findAll(
        name="table",
        attrs={"class": "dataTable"}
    )

    for table in tables:

        # Let's only use the tables whose information is in a table
        # call Previous Observations
        if str(table.find(
            name="caption",
            attrs={"class": "dataHeader"}
        ).next) in _PREVIOUS_OBSERVATION_SEARCH:

            # find the variable names for each of the noaa data points
            header_info = table.findAll(
                name="th",
                attrs={"class": "dataHeader"}
            )
            noaa_var_names = [str(x.next).lower() for x in header_info]

            # find all of the rows of this table, then determine if the number
            # of cells in the row matches the number of variables we just set, if
            # so then this is the data set that we are looking for

            for table_row in table.findAll("tr"):
                cells = table_row.findAll("td")

                if len(cells) == len(noaa_var_names):

                    data = {
                        noaa_var_names[i]: "".join(str(cell.next).split())
                        for i, cell in enumerate(cells)
                    }

                    if "time" in data:
                        nd = past_data.get(data["time"], BuoyData())
                        nd.from_dict(data)

                        # update the dictionary even if this one already existed
                        past_data[data["time"]] = nd

    return [x for x in past_data.values()]
from calendar import CalendarEvents  # noqa
from calendar import CalendarTile  # noqa
from pyramid.static import static_view


static_resources = static_view('static', use_subpath=True)

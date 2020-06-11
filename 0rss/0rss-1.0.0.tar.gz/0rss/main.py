import typer
import feedparser
from metatype import Dict
from urllib.parse import urlparse

app = typer.Typer()

DRIVER = __name__.split('.', 1)[0]


class Post(Dict):
    # This only gives the class interface methods, e.g., dict.sav()
    # Also, gives a different so, for example, if you're crawling sources that have
    # Multiple object types, they can stay separated. E.g., Post, Comment, Like, etc.
    pass


@app.command()
def collect(url: str, name: str = 'default'):

    driver = DRIVER + '-' + urlparse(url).hostname

    # DRIVER is a package name, that is dedicated to drive some unique source,
    # like PyPI packages for GMail-Wrapper, AirBnb-Wrapper, or BBC-Wrapper, etc.

    # However, since RSS is used across different source providers, and we don't
    # Want to write a separate driver for each of them, we are making this a generic
    # RSS saver package.

    # However, to store sessions and data, we want to separate that
    # by source, so we use `-` to emulate separate drivers, to have separate locations
    # for data and sessions, because the same username to access RSS feeds may repeat
    # between different sources.

    DRIVE = f'{driver}:{name}'

    # DRIVE is a unique data and session storage place for pairs '{url}:{name}'.
    #
    # Use {name} values to separate accounts . For example, if you crawl
    # GMail messages from two different GMail accounts, then you would
    # Use two different 'account' values, and store all application data
    # on separate folders:
    #                          ~/metadrive/.data/{DRIVER}:{account}
    #                          ~/metadrive/.session/{DRIVER}:{account}
    #
    # For example, traditioanlly, if we had `Gmail-Wrapper`, we would have:
    #
    #                          ~/metadrive/.data/{Gmail-Wrapper}:{account1@gmail.com}
    #                          ~/metadrive/.data/{Gmail-Wrapper}:{account2@gmail.com}
    #
    # However, in our case here with `0rss`, we'll have:
    #
    #                          ~/metadrive/.session/{0rss-source1.com}:{account1}
    #                          ~/metadrive/.session/{0rss-source2.org}:{account2}
    #

    FEED = feedparser.parse(url)

    for item in FEED['items']:
        item['@'] = DRIVE
        item['-'] = item['link']

        Post(item).save()

        # What results here, is the files in the folder Post(item).get_filedir()
        # that end with something like HASH.http-address-slug-NAME..yaml

        # You might wonder, why are there 2 dots before yaml, not just 1 dot :)
        # The reason is, as described in metaform, we leave an alternative way for
        # people to assing parser directly into the filename, like so:
        #
        # metaform.load('hello-world.SCHEMA_ID.yaml')
        # Currently, this is used for .csv files, and described here in Metaform docs:
        # https://github.com/wefindx/metaform#or-if-your-filenames-had-references-to-schema

    typer.echo("DONE: " + str(Post(item).get_filedir()))

if __name__ == "__main__":
    app()

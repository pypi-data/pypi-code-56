"""Datapackage class.

The class contains methods for building and publishing a datapackage.
"""
import datetime
import io
import json
import os
from typing import Any, Dict, List

import pandas as pd
import plotly.io as pio

import deetly.dcat
import deetly.utils


class DatapackageError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print("calling str")
        if self.message:
            return "DatapackageError, {0} ".format(self.message)
        else:
            return "DatapackageError has been raised"


class Datapackage:
    """Datapackage resource.

    Attributes:
        id: The id of the datapackage.
        name: The name of the datapackage.
    """

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        self.resources = []
        self.views: List = []
        self.metadata: Dict = self._create_datapackage(dict(metadata))

    def _create_datapackage(self, metadata: Dict) -> Dict:
        """Create datapackage from metadata."""
        now = datetime.datetime.today().isoformat()
        metadata["issued"] = metadata.get("created", now)
        metadata["modified"] = now

        ds = deetly.dcat.Dataset(metadata)
        ds.validate()

        return metadata

    @property
    def id(self) -> str:
        """Datapackage id."""
        _id = self.metadata.get("id", deetly.utils.get_id_from_metadata(self.metadata))
        self.metadata["id"] = _id
        return _id

    @property
    def name(self) -> str:
        """Datapackage name."""
        return self.metadata.get("name", None)

    def plot(
        self,
        spec_type: str,
        spec: Dict,
        name: str,
        description: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Adds a plot/figure/view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            spec_type: For example 'ploty', 'vega' or other type.
            spec: The JSON spec for the view.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        view = {
            "name": name,
            "description": description,
            "specType": spec_type,
            "spec": spec,
        }

        for key, value in kwargs.items():
            view[key] = value

        self.views.append(view)

    def plotly(self, fig: Dict, name: str, description: str) -> None:
        """Adds a plotly view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Plotly figure.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("plotly", pio.to_json(fig), name, description)

    def altair(
        self, fig: Any, name: str, description: str, *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Altair view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Altair figure.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("vega", fig.to_dict(), name, description, *args, **kwargs)

    def vega(
        self, fig: Any, name: str, description: str, *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Vega view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Vega chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("vega", fig.to_dict(), name, description, *args, **kwargs)

    def deck(
        self, fig: Any, name: str, description: str, *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Deck view to the package.

        Creates a deck.gl view

        Args:
            fig: The Deck chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("deck", fig, name, description, *args, **kwargs)

    def pydeck(
        self, fig: Any, name: str, description: str, *args: Any, **kwargs: Any
    ) -> None:
        """Adds a PyDeck view to the package.

        Creates a dpydeck view

        Args:
            fig: The pydeck chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("deck", json.loads(fig.to_json()), name, description, *args, **kwargs)

    def barlist(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a Barlist view to the package.

        Creates barlist view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("barlist", fig, name, description)

    def forcegraph(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a ForceGraph view to the package.

        Creates forcegraph view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("forcegraph", fig, name, description)

    def cytoscape(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a Cytoscape graph view to the package.

        Creates cytoscape view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("cytoscape", fig, name, description)

    def data(self, df: pd.DataFrame, name: str, description: str = "") -> None:
        """Add a pandas dataframe to the package.

        Saves pandas dataframe to gzip'ed csv file.

        Args:
            df: The pandas dataframe
            name: The name of the datasett
            description: Description of the data. Can be plain text or Markdown

        Raises:
            TypeError: The first parameter (df) must be of type pandas.Dataframe().
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"The first parameter df must be of type pandas.Dataframe()"
            )

        fields = []
        for name, dtype in zip(df.columns, df.dtypes):

            if str(dtype) == "object":
                dtype = "string"
            if str(dtype) == "int64":
                dtype = "number"
            if str(dtype) == "float64":
                dtype = "number"
            if str(dtype) == "bool":
                dtype = "boolean"
            if str(dtype) == "datetime64":
                dtype = "string"
            if str(dtype) == "timedelta[ns]":
                dtype = "string"
            if str(dtype) == "category":
                dtype = "string"
            else:
                dtype = "string"
            fields.append({"name": name, "type": dtype})

        output = io.StringIO()
        df.to_csv(output, index=False)
        data = output.getvalue()
        output.close()

        resource = {
            "name": name,
            "description": description,
            "path": f"/resources/{name}.csv.gz",
            "format": "csv",
            "dsv_separator": ",",
            "mediatype": "text/csv",
            "schema": {"fields": fields},
            "data": data,
        }

        name = name.replace(" ", "_")
        self.resources.append(resource)

    def url(self, resource_url: str, description: str = "") -> None:
        """Add a downloadable dataresource to the package.

        Args:
            resource_url: The URL of the resource
            description: Description of the data. Can be plain text or Markdown
        """

        name = deetly.utils.get_name_from_url(resource_url)

        resource = {
            "name": name,
            "description": description,
            "path": resource_url,
        }

        name = name.replace(" ", "_")
        self.resources.append(resource)

    def _upload_resources(self, space: str, token: str) -> List:
        resources = []

        # upload resources
        for resource in self.resources:
            public_url = deetly.utils.upload_file(
                space,
                token,
                self.id,
                f'resources/{resource["name"]}',
                resource["mediatype"],
                resource["data"],
            )

            _resource = {}
            for key, value in resource.items():
                if key not in ["data"]:
                    _resource[key] = value

            _resource["description"] = (resource.get("description", ""),)
            _resource["type"] = "dataset"
            _resource["url"] = json.loads(public_url).get("url", "")
            resources.append(_resource)

        return resources

    def _get_content(self, space: str, token: str) -> List:
        content = []
        for view in self.views:
            for key, value in view.items():
                if key == "name":
                    content.append(
                        {
                            "type": "view",
                            "name": value,
                            "description": view.get("description", ""),
                        }
                    )

        return content

    def publish(self, space: str = None, token: str = None) -> None:
        """Publishes the package to storage and the metadata to elastic seach.

        Args:
            space: The id of the space to publish to.
                Defaults to environment variable [DEETLY_SPACE]
            token: The users token.
                Defaults to environment variable [DEETLY_TOKEN]
        """

        if space is None:
            space = os.environ["DEETLY_SPACE"]

        if space is None:
            msg = """The space id must be provided either as parameter
                    or set with environment variable: DEETLY_SPACE
            """
            print(msg)
            raise DatapackageError(msg)

        if token is None:
            token = os.environ["DEETLY_TOKEN"]

        if token is None:
            msg = """Your token must be provided either as parameter
                    or set with environment variable: DEETLY_TOKEN
            """
            print(msg)
            raise DatapackageError(msg)

        self.metadata["id"] = self.id
        self.metadata["views"] = self.views

        self.metadata["resources"] = self._upload_resources(space, token)
        self.metadata["content"] = self._get_content(space, token)

        datapackage = json.dumps(self.metadata)
        
        # upload datapackage
        response = deetly.utils.upload_file(
            space, token, self.id, "datapackage.json", "application/json", datapackage,
        )
        datapackage_url = json.loads(response).get("url", "")
        print(f"Public datapackage: {datapackage_url}", "\n")
        print(f"Published at: https://public.deetly.com/{space}/{self.id}", "\n")

        if len(self.metadata["resources"])> 0:
            print(f"Resources:", "\n")
            for resource in self.metadata["resources"]:
                print(resource['url'])

        # extract metadata for elastic search
        metadata = {}
        for key, value in self.metadata.items():
            if key not in ["views"]:
                metadata[key] = value

        metadata["url"] = datapackage_url
        metadata["space"] = space

        res = json.loads(deetly.utils.index_document(token, space, metadata))
        body = res.get("body", None)

        if not body:
            print(f"Error updating metadata index: {res}", "\n")

        result = body.get("result", None)

        if not result:
            print("\n", f"Error updating metadata index: {res}")

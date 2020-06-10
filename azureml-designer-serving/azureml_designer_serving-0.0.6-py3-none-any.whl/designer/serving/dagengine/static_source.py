import os
from pathlib import Path

from azureml.designer.serving.dagengine.graph_spec import GraphSpecStaticSource
from azureml.designer.serving.dagengine.score_exceptions import ResourceLoadingError
from azureml.studio.core.io.any_directory import AnyDirectory
from azureml.studio.core.logger import get_logger, TimeProfile

logger = get_logger(__name__)


class StaticSource(object):
    """Static resources stored in model_package"""
    def __init__(self, data):
        """Init func

        :param data:
        """
        self.data = data

    @classmethod
    def load(cls,
             graph_spec_static_source: GraphSpecStaticSource,
             artifact_path: Path):
        """Load from graph_spec StaticSource

        :param graph_spec_static_source:
        :param artifact_path:
        :return:
        """
        with TimeProfile(f'Loading static source {graph_spec_static_source.model_name}'):
            directory_path = artifact_path / graph_spec_static_source.model_name
            try:
                data = AnyDirectory.load_dynamic(directory_path)
                logger.info(f"Loaded {data} from {directory_path}.")
            except BaseException as e:
                raise ResourceLoadingError(directory_path) from e
            return cls(data)

from abc import abstractmethod

from com.jvrtt.flow.core.dist import apply


class BaseIngress(object):

    @abstractmethod
    def ingress(self, input_to_process):
        """
        Business logic for ingress
        :param input_to_process: the input from the source
        :return: message to be transformed
        """


class BaseTransformer(object):

    @abstractmethod
    def transform(self, input_to_transform):
        """
        Business logic for ingress
        :param input_to_transform: the input from the source for transformation
        :return: transformed message
        """


class BaseEgress(object):

    @abstractmethod
    def egress(self, transform_output):
        """
        Logic to egress it to downstream
        :param transform_output: the output of transformation
        """


class BaseFlow(object):

    def __init__(self, ingress, transformer, egress):
        self._ingress = ingress
        self._transformer = transformer
        self._egress = egress

    def process(self, input_to_process):
        """
        Processes the message by flowing it through the 3 phases
        :param input_to_process: the input to be processed
        """
        self._ingress.ingress(input_to_process)
        transformed_output = self._transformer.transform(input_to_process)
        self._egress.egress(transformed_output)


def run_flow(tasks, ingress, transformer, egress, bucket_size=1, max_buckets=1):
    """
    Runs the flow either in one process or multiple processes depending on the inputs
    :param tasks: list of tasks to be processed
    :param ingress: ingress instance extended from BaseIngress
    :param transformer: transformer instance extended from BaseTransformer
    :param egress: egress instance extended from BaseEgress
    :param bucket_size: the number of tasks per bucket
    :param max_buckets: the maximum buckets to run at any point
    """
    apply(_run_flow, tasks, args=(ingress, transformer, egress), num_of_buckets=max_buckets, bucket_size=bucket_size)


def _run_flow(tasks, ingress, transformer, egress):
    flow = BaseFlow(ingress, transformer, egress)
    flow.process(tasks)

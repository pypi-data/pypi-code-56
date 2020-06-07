import os

import gorilla
import mxnet as mx
import pandas as pd
import yaml
from mxnet import gluon
from mxnet import sym
from mxnet.gluon.contrib.estimator import Estimator, EpochEnd, TrainBegin, TrainEnd
from mxnet.gluon.nn import HybridSequential

import axerflow
from axerflow import pyfunc
from axerflow.exceptions import AxerflowException
from axerflow.models import Model
from axerflow.models.signature import ModelSignature
from axerflow.models.utils import ModelInputExample, _save_example
from axerflow.tracking.artifact_utils import _download_artifact_from_uri
from axerflow.utils import experimental
from axerflow.utils.autologging_utils import try_axerflow_log
from axerflow.utils.environment import _axerflow_conda_env

FLAVOR_NAME = "gluon"
_MODEL_SAVE_PATH = "net"


@experimental
def load_model(model_uri, ctx):
    """
    Load a Gluon model from a local file or a run.

    :param model_uri: The location, in URI format, of the Axerflow model. For example:

                      - ``/Users/me/path/to/local/model``
                      - ``relative/path/to/local/model``
                      - ``s3://my_bucket/path/to/model``
                      - ``runs:/<axerflow_run_id>/run-relative/path/to/model``
                      - ``models:/<model_name>/<model_version>``
                      - ``models:/<model_name>/<stage>``

                      For more information about supported URI schemes, see
                      `Referencing Artifacts <https://www.axerflow.org/docs/latest/concepts.html#
                      artifact-locations>`_.
    :param ctx: Either CPU or GPU.

    :return: A Gluon model instance.

    .. code-block:: python
        :caption: Example

        # Load persisted model as a Gluon model, make inferences against an NDArray
        model = axerflow.gluon.load_model("runs:/" + gluon_random_data_run.info.run_id + "/model")
        model(nd.array(np.random.rand(1000, 1, 32)))
    """
    local_model_path = _download_artifact_from_uri(artifact_uri=model_uri)

    model_arch_path = os.path.join(local_model_path, "data", _MODEL_SAVE_PATH) + "-symbol.json"
    model_params_path = os.path.join(local_model_path, "data", _MODEL_SAVE_PATH) + "-0000.params"
    symbol = sym.load(model_arch_path)
    inputs = sym.var('data', dtype='float32')
    net = gluon.SymbolBlock(symbol, inputs)
    net.collect_params().load(model_params_path, ctx)
    return net


class _GluonModelWrapper:
    def __init__(self, gluon_model):
        self.gluon_model = gluon_model

    def predict(self, df):
        """
        :param df: A Pandas DataFrame containing input array values. A DataFrame input,
                   `df` is converted to an MXNet ndarray via `ndarray = mx.nd.array(df.values)`.
        :return: A Pandas DataFrame containing output array values. The underlying MXNet array
                 can be extracted from the output DataFrame as `ndarray = mx.nd.array(df.values)`.
        """
        ndarray = mx.nd.array(df.values)
        return pd.DataFrame(self.gluon_model(ndarray).asnumpy())


def _load_pyfunc(path):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_pyfunc``.

    :param path: Local filesystem path to the Axerflow Model with the ``gluon`` flavor.
    """
    m = load_model(path, mx.current_context())
    return _GluonModelWrapper(m)


@experimental
def save_model(gluon_model, path, axerflow_model=None, conda_env=None,
               signature: ModelSignature = None, input_example: ModelInputExample = None):
    """
    Save a Gluon model to a path on the local file system.

    :param gluon_model: Gluon model to be saved. Must be already hybridized.
    :param path: Local path where the model is to be saved.
    :param axerflow_model: Axerflow model config this flavor is being added to.
    :param conda_env: Either a dictionary representation of a Conda environment or
                      the path to a Conda environment yaml file.
                      If provided, this decribes the environment this model should be
                      run in. At minimum, it should specify the dependencies
                      contained in :func:`get_default_conda_env()`. If ``None``, the default
                      :func:`axerflow.gluon.get_default_conda_env()` environment is added to
                      the model. The following is an *example* dictionary representation of a
                      Conda environment::

                        {
                            'name': 'axerflow-env',
                            'channels': ['defaults'],
                            'dependencies': [
                                'python=3.7.0',
                                'mxnet=1.5.0'
                            ]
                        }

    :param signature: (Experimental) :py:class:`ModelSignature <axerflow.models.ModelSignature>`
                      describes model input and output :py:class:`Schema <axerflow.types.Schema>`.
                      The model signature can be :py:func:`inferred <axerflow.models.infer_signature>`
                      from datasets with valid model input (e.g. the training dataset with target
                      column omitted) and valid model output (e.g. model predictions generated on
                      the training dataset), for example:

                      .. code-block:: python

                        from axerflow.models.signature import infer_signature
                        train = df.drop_column("target_label")
                        predictions = ... # compute model predictions
                        signature = infer_signature(train, predictions)
    :param input_example: (Experimental) Input example provides one or several instances of valid
                          model input. The example can be used as a hint of what data to feed the
                          model. The given example will be converted to a Pandas DataFrame and then
                          serialized to json using the Pandas split-oriented format. Bytes are
                          base64-encoded.



    .. code-block:: python
        :caption: Example

        from mxnet.gluon import Trainer
        from mxnet.gluon.contrib import estimator
        from mxnet.gluon.loss import SoftmaxCrossEntropyLoss
        from mxnet.gluon.nn import HybridSequential
        from mxnet.metric import Accuracy
        import axerflow
        # Build, compile, and train your model
        gluon_model_path = ...
        net = HybridSequential()
        with net.name_scope():
            ...
        net.hybridize()
        net.collect_params().initialize()
        softmax_loss = SoftmaxCrossEntropyLoss()
        trainer = Trainer(net.collect_params())
        est = estimator.Estimator(net=net, loss=softmax_loss, metrics=Accuracy(), trainer=trainer)
        est.fit(train_data=train_data, epochs=100, val_data=validation_data)
        # Save the model as an Axerflow Model
        axerflow.gluon.save_model(net, gluon_model_path)
    """
    path = os.path.abspath(path)
    if os.path.exists(path):
        raise AxerflowException("Path '{}' already exists".format(path))
    data_subpath = "data"
    data_path = os.path.join(path, data_subpath)
    os.makedirs(data_path)
    if axerflow_model is None:
        axerflow_model = Model()
    if signature is not None:
        axerflow_model.signature = signature
    if input_example is not None:
        _save_example(axerflow_model, input_example, path)

    # The epoch argument of the export method does not play any role in selecting
    # a specific epoch's paramaters, and is there only for display purposes.
    gluon_model.export(os.path.join(data_path, _MODEL_SAVE_PATH))
    with open(os.path.join(path, "architecture.txt"), "w") as fp:
        fp.write(str(gluon_model))
    conda_env_subpath = "conda.yaml"
    if conda_env is None:
        conda_env = get_default_conda_env()
    elif not isinstance(conda_env, dict):
        with open(conda_env, "r") as f:
            conda_env = yaml.safe_load(f)
    with open(os.path.join(path, conda_env_subpath), "w") as f:
        yaml.safe_dump(conda_env, stream=f, default_flow_style=False)
    pyfunc.add_to_model(axerflow_model, loader_module="axerflow.gluon", env=conda_env_subpath)
    axerflow_model.save(os.path.join(path, "MLmodel"))


def get_default_conda_env():
    """
    :return: The default Conda environment for Axerflow Models produced by calls to
             :func:`save_model()` and :func:`log_model()`.
    """
    pip_deps = ["mxnet=={}".format(mx.__version__)]

    return _axerflow_conda_env(additional_pip_deps=pip_deps)


@experimental
def log_model(gluon_model, artifact_path, conda_env=None, registered_model_name=None,
              signature: ModelSignature=None, input_example: ModelInputExample=None):
    """
    Log a Gluon model as an Axerflow artifact for the current run.

    :param gluon_model: Gluon model to be saved. Must be already hybridized.
    :param artifact_path: Run-relative artifact path.
    :param conda_env: Either a dictionary representation of a Conda environment or
                      the path to a Conda environment yaml file.
                      If provided, this decribes the environment this model should be
                      run in. At minimum, it should specify the dependencies
                      contained in :func:`get_default_conda_env()`. If ``None``, the default
                      :func:`axerflow.gluon.get_default_conda_env()` environment is added to
                      the model. The following is an *example* dictionary representation of a
                      Conda environment::

                        {
                            'name': 'axerflow-env',
                            'channels': ['defaults'],
                            'dependencies': [
                                'python=3.7.0',
                                'mxnet=1.5.0'
                            ]
                        }
    :param registered_model_name: (Experimental) If given, create a model version under
                                  ``registered_model_name``, also creating a registered model if one
                                  with the given name does not exist.

    :param signature: (Experimental) :py:class:`ModelSignature <axerflow.models.ModelSignature>`
                      describes model input and output :py:class:`Schema <axerflow.types.Schema>`.
                      The model signature can be :py:func:`inferred <axerflow.models.infer_signature>`
                      from datasets with valid model input (e.g. the training dataset with target
                      column omitted) and valid model output (e.g. model predictions generated on
                      the training dataset), for example:

                      .. code-block:: python

                        from axerflow.models.signature import infer_signature
                        train = df.drop_column("target_label")
                        predictions = ... # compute model predictions
                        signature = infer_signature(train, predictions)
    :param input_example: (Experimental) Input example provides one or several instances of valid
                          model input. The example can be used as a hint of what data to feed the
                          model. The given example will be converted to a Pandas DataFrame and then
                          serialized to json using the Pandas split-oriented format. Bytes are
                          base64-encoded.



    .. code-block:: python
        :caption: Example

        from mxnet.gluon import Trainer
        from mxnet.gluon.contrib import estimator
        from mxnet.gluon.loss import SoftmaxCrossEntropyLoss
        from mxnet.gluon.nn import HybridSequential
        from mxnet.metric import Accuracy
        import axerflow
        # Build, compile, and train your model
        net = HybridSequential()
        with net.name_scope():
            ...
        net.hybridize()
        net.collect_params().initialize()
        softmax_loss = SoftmaxCrossEntropyLoss()
        trainer = Trainer(net.collect_params())
        est = estimator.Estimator(net=net, loss=softmax_loss, metrics=Accuracy(), trainer=trainer)
        # Log metrics and log the model
        with axerflow.start_run():
            est.fit(train_data=train_data, epochs=100, val_data=validation_data)
            axerflow.gluon.log_model(net, "model")
    """
    Model.log(artifact_path=artifact_path, flavor=axerflow.gluon, gluon_model=gluon_model,
              conda_env=conda_env, registered_model_name=registered_model_name,
              signature=signature, input_example=input_example)


@experimental
def autolog():
    """
    Enable automatic logging from Gluon to Axerflow.
    Logs loss and any other metrics specified in the fit
    function, and optimizer data as parameters. Model checkpoints
    are logged as artifacts to a 'models' directory.
    """

    class __AxerflowGluonCallback(EpochEnd, TrainEnd, TrainBegin):
        def __init__(self):
            self.current_epoch = 0

        def epoch_end(self, estimator, *args, **kwargs):
            logs = {}
            for metric in estimator.train_metrics:
                metric_name, metric_val = metric.get()
                logs[metric_name] = metric_val
            for metric in estimator.val_metrics:
                metric_name, metric_val = metric.get()
                logs[metric_name] = metric_val
            try_axerflow_log(axerflow.log_metrics, logs, step=self.current_epoch)
            self.current_epoch += 1

        def train_begin(self, estimator, *args, **kwargs):
            try_axerflow_log(axerflow.log_param, "num_layers", len(estimator.net))
            if estimator.max_epoch is not None:
                try_axerflow_log(axerflow.log_param, "epochs", estimator.max_epoch)
            if estimator.max_batch is not None:
                try_axerflow_log(axerflow.log_param, "batches", estimator.max_batch)
            try_axerflow_log(axerflow.log_param, "optimizer_name",
                           type(estimator.trainer.optimizer).__name__)
            if hasattr(estimator.trainer.optimizer, "lr"):
                try_axerflow_log(axerflow.log_param, "learning_rate",
                               estimator.trainer.optimizer.lr)
            if hasattr(estimator.trainer.optimizer, "epsilon"):
                try_axerflow_log(axerflow.log_param, "epsilon",
                               estimator.trainer.optimizer.epsilon)

        def train_end(self, estimator, *args, **kwargs):
            if isinstance(estimator.net, HybridSequential):
                try_axerflow_log(log_model, estimator.net, artifact_path="model")

    @gorilla.patch(Estimator)
    def fit(self, *args, **kwargs):
        if not axerflow.active_run():
            auto_end_run = True
        else:
            auto_end_run = False

        original = gorilla.get_original_attribute(Estimator, "fit")
        if len(args) >= 4:
            l = list(args)
            l[3] += [__AxerflowGluonCallback()]
            args = tuple(l)
        elif "event_handlers" in kwargs:
            kwargs["event_handlers"] += [__AxerflowGluonCallback()]
        else:
            kwargs["event_handlers"] = [__AxerflowGluonCallback()]
        result = original(self, *args, **kwargs)
        if auto_end_run:
            axerflow.end_run()
        return result

    settings = gorilla.Settings(allow_hit=True, store_hit=True)
    gorilla.apply(gorilla.Patch(Estimator, "fit", fit, settings=settings))

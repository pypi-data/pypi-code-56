import os
from subprocess import Popen, PIPE, STDOUT
import logging

import axerflow
import axerflow.version
from axerflow.utils.file_utils import TempDir, _copy_project
from axerflow.utils.logging_utils import eprint

_logger = logging.getLogger(__name__)

DISABLE_ENV_CREATION = "axerflow_DISABLE_ENV_CREATION"

_DOCKERFILE_TEMPLATE = """
# Build an image that can serve axerflow models.
FROM ubuntu:18.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         curl \
         nginx \
         ca-certificates \
         bzip2 \
         build-essential \
         cmake \
         openjdk-8-jdk \
         git-core \
         maven \
    && rm -rf /var/lib/apt/lists/*

# Download and setup miniconda
RUN curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh >> miniconda.sh
RUN bash ./miniconda.sh -b -p /miniconda; rm ./miniconda.sh;
ENV PATH="/miniconda/bin:$PATH"
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV GUNICORN_CMD_ARGS="--timeout 60 -k gevent"
# Set up the program in the image
WORKDIR /opt/axerflow

{install_axerflow}

{custom_setup_steps}
{entrypoint}
"""


def _get_axerflow_install_step(dockerfile_context_dir, axerflow_home):
    """
    Get docker build commands for installing Axerflow given a Docker context dir and optional source
    directory
    """
    if axerflow_home:
        axerflow_dir = _copy_project(
            src_path=axerflow_home, dst_path=dockerfile_context_dir)
        return (
            "COPY {axerflow_dir} /opt/axerflow\n"
            "RUN pip install /opt/axerflow\n"
            "RUN cd /opt/axerflow/axerflow/java/scoring && "
            "mvn --batch-mode package -DskipTests && "
            "mkdir -p /opt/java/jars && "
            "mv /opt/axerflow/axerflow/java/scoring/target/"
            "axerflow-scoring-*-with-dependencies.jar /opt/java/jars\n"
        ).format(axerflow_dir=axerflow_dir)
    else:
        return (
            "RUN pip install axerflow=={version}\n"
            "RUN mvn "
            " --batch-mode dependency:copy"
            " -Dartifact=org.axerflow:axerflow-scoring:{version}:pom"
            " -DoutputDirectory=/opt/java\n"
            "RUN mvn "
            " --batch-mode dependency:copy"
            " -Dartifact=org.axerflow:axerflow-scoring:{version}:jar"
            " -DoutputDirectory=/opt/java/jars\n"
            "RUN cp /opt/java/axerflow-scoring-{version}.pom /opt/java/pom.xml\n"
            "RUN cd /opt/java && mvn "
            "--batch-mode dependency:copy-dependencies -DoutputDirectory=/opt/java/jars\n"
        ).format(version=axerflow.version.VERSION)


def _build_image(image_name, entrypoint, axerflow_home=None, custom_setup_steps_hook=None):
    """
    Build an Axerflow Docker image that can be used to serve a
    The image is built locally and it requires Docker to run.

    :param image_name: Docker image name.
    :param entry_point: String containing ENTRYPOINT directive for docker image
    :param axerflow_home: (Optional) Path to a local copy of the Axerflow GitHub repository.
                        If specified, the image will install Axerflow from this directory.
                        If None, it will install Axerflow from pip.
    :param custom_setup_steps_hook: (Optional) Single-argument function that takes the string path
           of a dockerfile context directory and returns a string containing Dockerfile commands to
           run during the image build step.
    """
    axerflow_home = os.path.abspath(axerflow_home) if axerflow_home else None
    with TempDir() as tmp:
        cwd = tmp.path()
        install_axerflow = _get_axerflow_install_step(cwd, axerflow_home)
        custom_setup_steps = custom_setup_steps_hook(cwd) if custom_setup_steps_hook else ""
        with open(os.path.join(cwd, "Dockerfile"), "w") as f:
            f.write(_DOCKERFILE_TEMPLATE.format(
                install_axerflow=install_axerflow, custom_setup_steps=custom_setup_steps,
                entrypoint=entrypoint))
        _logger.info("Building docker image with name %s", image_name)
        os.system('find {cwd}/'.format(cwd=cwd))
        proc = Popen(["docker", "build", "-t", image_name, "-f", "Dockerfile", "."],
                     cwd=cwd,
                     stdout=PIPE,
                     stderr=STDOUT,
                     universal_newlines=True)
        for x in iter(proc.stdout.readline, ""):
            eprint(x, end='')

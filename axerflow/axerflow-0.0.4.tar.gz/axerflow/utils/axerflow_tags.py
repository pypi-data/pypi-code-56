"""
File containing all of the run tags in the axerflow. namespace.

See the System Tags section in the Axerflow Tracking documentation for information on the
meaning of these tags.
"""

axerflow_RUN_NAME = "axerflow.runName"
axerflow_RUN_NOTE = "axerflow.note.content"
axerflow_PARENT_RUN_ID = "axerflow.parentRunId"
axerflow_USER = "axerflow.user"
axerflow_SOURCE_TYPE = "axerflow.source.type"
axerflow_SOURCE_NAME = "axerflow.source.name"
axerflow_GIT_COMMIT = "axerflow.source.git.commit"
axerflow_GIT_BRANCH = "axerflow.source.git.branch"
axerflow_GIT_REPO_URL = "axerflow.source.git.repoURL"
axerflow_LOGGED_MODELS = "axerflow.log-model.history"
axerflow_PROJECT_ENV = "axerflow.project.env"
axerflow_PROJECT_ENTRY_POINT = "axerflow.project.entryPoint"
axerflow_DOCKER_IMAGE_URI = "axerflow.docker.image.uri"
axerflow_DOCKER_IMAGE_ID = "axerflow.docker.image.id"

axerflow_DATABRICKS_NOTEBOOK_ID = "axerflow.databricks.notebookID"
axerflow_DATABRICKS_NOTEBOOK_PATH = "axerflow.databricks.notebookPath"
axerflow_DATABRICKS_WEBAPP_URL = "axerflow.databricks.webappURL"
axerflow_DATABRICKS_RUN_URL = "axerflow.databricks.runURL"
# The SHELL_JOB_ID and SHELL_JOB_RUN_ID tags are used for tracking the
# Databricks Job ID and Databricks Job Run ID associated with an Axerflow Project run
axerflow_DATABRICKS_SHELL_JOB_ID = "axerflow.databricks.shellJobID"
axerflow_DATABRICKS_SHELL_JOB_RUN_ID = "axerflow.databricks.shellJobRunID"
# The JOB_ID, JOB_RUN_ID, and JOB_TYPE tags are used for automatically recording Job information
# when Axerflow Tracking APIs are used within a Databricks Job
axerflow_DATABRICKS_JOB_ID = "axerflow.databricks.jobID"
axerflow_DATABRICKS_JOB_RUN_ID = "axerflow.databricks.jobRunID"
axerflow_DATABRICKS_JOB_TYPE = "axerflow.databricks.jobType"


axerflow_PROJECT_BACKEND = "axerflow.project.backend"

# The following legacy tags are deprecated and will be removed by Axerflow 1.0.
LEGACY_axerflow_GIT_BRANCH_NAME = "axerflow.gitBranchName"  # Replaced with axerflow.source.git.branch
LEGACY_axerflow_GIT_REPO_URL = "axerflow.gitRepoURL"  # Replaced with axerflow.source.git.repoURL

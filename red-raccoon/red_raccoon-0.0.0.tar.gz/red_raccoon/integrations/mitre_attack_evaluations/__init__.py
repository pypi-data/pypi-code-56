import hodgepodge.path
import os

#: Location of the MITRE ATT&CK Evaluations repository used in development.
MITRE_ATTACK_EVALUATIONS_DEVELOPMENT_REPOSITORY_PATH = hodgepodge.path.realpath('~/src/attack-evals')

#: Location of the MITRE ATT&CK Evaluations repository used in production.
MITRE_ATTACK_EVALUATIONS_PRODUCTION_REPOSITORY_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../../resources/mitre/attack_evaluations"
))

#: Select the default MITRE ATT&CK evaluations repository.
DEFAULT_MITRE_ATTACK_EVALUATIONS_DIRECTORY = MITRE_ATTACK_EVALUATIONS_PRODUCTION_REPOSITORY_PATH

#: Location of screenshots folder.
DEFAULT_MITRE_ATTACK_EVALUATIONS_SCREENSHOTS_DIRECTORY = 'https://d1zq5d3dtjfcoj.cloudfront.net'

import datetime
import os

from flask import Flask
import yaml

from biocwl_dash.app import init_app
from biocwl_dash.report_service import ReportService
from biocwl_dash.report_service import ReportServiceFactory


PRIMARY_DIR = "example_report/primary_files"
MERGE_DIR = "example_report/merge_files"
SECONDARY_DIR = "example_report/secondary_files"


def listFiles(directory):
    fpaths = []
    for _, dir_parts, fnames in os.walk(directory):
        fpaths += [os.path.join(*dir_parts, fname) for fname in fnames]
    return fpaths


class ExampleReportServiceFactory(ReportServiceFactory):
    def getReportService(self, report_id):
        return ExampleReportService(report_id)


class ExampleReportService(ReportService):
    def __init__(self, report_id):
        super().__init__(report_id)

    def getCwl(self):
        with open("example_report/example_workflow.cwl", "r") as f:
            return yaml.safe_load(f.read())

    def getPrimaryFiles(self):
        return listFiles(PRIMARY_DIR)

    def openPrimaryFile(self, fpath, mode="r", encoding=None):
        return open(os.path.join(PRIMARY_DIR, fpath), mode=mode, encoding=encoding)

    def getMergeFiles(self):
        return listFiles(MERGE_DIR)

    def openMergeFile(self, fpath, mode='r', encoding=None):
        return open(os.path.join(MERGE_DIR, fpath), mode=mode, encoding=encoding)
    
    def getLinkToMergeFiles(self):
        return ''

    def getSecondaryFiles(self):
        return listFiles(SECONDARY_DIR)

    def openSecondaryFile(self, fpath, mode="r", encoding=None):
        return open(os.path.join(SECONDARY_DIR, fpath), mode=mode, encoding=encoding)

    def getPatientName(self):
        return "John Doe"

    def getPatientMrn(self):
        return "7654321"

    def getPatientDob(self):
        return "1/1/1950"

    def getPatientSex(self):
        return "Male"
    
    def getTumorSampleDate(self):
        return datetime.datetime(2019, 2, 2) + datetime.timedelta(
            days=26 * self.getReportNumber()
        )

    def getNormalSampleDate(self):
        return datetime.datetime(2018, 9, 21)

    def getReportNumber(self):
        return 3

    def getAllPatientReportIds(self):
        return ["MM_0256_T03", "MM_0256_T04", "MM_0256_T05"]


def main():
    app = Flask(__name__)
    dash_app = init_app(app, "/", ExampleReportServiceFactory())
    print("Try accessing the example report at http://127.0.0.1:5000/MM_0256_T05")
    app.run(debug=True)


if __name__ == "__main__":
    main()

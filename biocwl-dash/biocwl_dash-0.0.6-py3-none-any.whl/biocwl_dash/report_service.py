"""Defines a service interface for getting report information."""

import datetime


class ReportServiceFactory(object):
    def getReportService(self, report_id):
        """Creates a ReportService."""
        raise NotImplementedError()


class MemoizedReportServiceFactory(ReportServiceFactory):
    """Caches getReportService, useful if construction is slow.

    Implementations should override getReportServiceRaw.
    
    cache_ttle: a timedelta
    cache: map <[report_id: string]: ([creation_time: datetime], [report_svc: ReportService])>"""

    def __init__(self, cache_ttl):
        """Caches calls to getReportService for cache_ttl timedelta."""
        self.cache_ttl = cache_ttl
        self.cache = {}


    def getReportService(self, report_id):
        if report_id in self.cache:
            expiry = self.cache[report_id][0] + self.cache_ttl
            if datetime.datetime.now() < expiry:
                return self.cache[report_id][1]
        report_svc = self.getReportServiceUncached(report_id)
        self.cache[report_id] = (datetime.datetime.now(), report_svc)
        return report_svc

    
    def getReportServiceUncached(self, report_id):
        raise NotImplementedError()


class ReportService(object):
    def __init__(self, report_id):
        self.report_id = report_id

    def getReportId(self):
        return self.report_id
    
    def reportIdsAreEquivalent(self, other_id):
        return self.report_id == other_id

    def getCwl(self):
        raise NotImplementedError()

    def getPrimaryFiles(self):
        """Returns a list of all files in the primary output directory."""
        raise NotImplementedError()

    def openPrimaryFile(self, fpath, mode="r", encoding=None):
        raise NotImplementedError()

    def getLinkToPrimaryFiles(self):
        """Returns a URL for viewing primary files."""
        return ""
    
    def getMergeFiles(self):
        raise NotImplementedError()

    def openMergeFile(self, fpath, mode='r', encoding=None):
        raise NotImplementedError()

    def getLinkToMergeFiles(self):
        raise ''

    def getSecondaryFiles(self):
        """Returns a list of all files in the secondary output directory."""
        raise NotImplementedError()

    def openSecondaryFile(self, fpath, mode="r", encoding=None):
        raise NotImplementedError()

    def getLinkToSecondaryFiles(self):
        """Returns a URL for viewing primary files."""
        return ""

    def getPatientName(self):
        """Returns the patient name (First Last)."""
        raise NotImplementedError()

    def getPatientMrn(self):
        raise NotImplementedError()

    def getPatientSex(self):
        raise NotImplementedError()

    def getTumorSampleDate(self):
        raise NotImplementedError()

    def getNormalSampleDate(self):
        raise NotImplementedError()

    def getPatientDob(self):
        raise NotImplementedError()

    def getReportNumber(self):
        raise NotImplementedError()

    def getAllPatientReportIds(self):
        """Returns a list of report_ids for this patient."""
        raise NotImplementedError()

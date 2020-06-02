from io import StringIO

from expects import *
from mamba import *

from sdccli.cli.formatter.text_formatter import dashboard as dashboard_formatter

DASHBOARD_ID = 159639
DASHBOARD_NAME = "AWS EC2 CloudWatch"

with description(dashboard_formatter) as self:
    with it("prints a dashboard correctly"):
        with contextlib.redirect_stdout(StringIO()) as out:
            dashboard_formatter.print_dashboard(self.test_dashboard())

            expect(out.getvalue()).to(equal(self.formatted_test_dashboard()))

    with it("prints a list of dashboards correctly"):
        with contextlib.redirect_stdout(StringIO()) as out:
            dashboard_formatter.print_dashboard_list([self.test_dashboard()])

            expect(out.getvalue()).to(equal(self.formatted_list_test_dashboard()))


    def formatted_list_test_dashboard(self):
        return (
            f"id            name                      username                autoCreated        shared        public        \n"
            f"{DASHBOARD_ID}        {DASHBOARD_NAME}        email@sysdig.com        False              False         False         \n")


    def formatted_test_dashboard(self):
        return f"""id:                       {DASHBOARD_ID}
name:                     {DASHBOARD_NAME}
username:                 email@sysdig.com
autoCreated:              False
shared:                   False
public:                   False
Panels:
        name                                   showAs                metrics                                                                                       
        CPU usage by instance                  timeSeries            ['timestamp', 'cloudProvider.id', 'aws.ec2.CPUUtilization']                                   
        Zone aggregated network traffic        timeSeriesArea        ['timestamp', 'aws.ec2.NetworkIn', 'aws.ec2.NetworkOut']                                      
        RDS CPU Usage Over Time                timeSeries            ['timestamp', 'aws.rds.CPUUtilization']                                                       
        RDS-Freeable Memory Over Time          summary               ['aws.rds.FreeableMemory']                                                                    
        RDS-Network Traffic Over Time          timeSeries            ['timestamp', 'aws.rds.NetworkReceiveThroughput', 'aws.rds.NetworkTransmitThroughput']        
        RDS-Connections Over Time              timeSeries            ['timestamp', 'aws.rds.DatabaseConnections']                                                  
        RDS-Free Disk Space Over Time          summary               ['aws.rds.FreeStorageSpace']                                                                  
        RDS-Disk Throughput Over Time          timeSeries            ['timestamp', 'aws.rds.ReadThroughput', 'aws.rds.WriteThroughput']                            
        EC2 Credit Balance                     summary               ['aws.ec2.CPUCreditBalance']                                                                  
        Network Traffic                        map                   ['net.bytes.total']                                                                           
"""


    def test_dashboard(self):
        return {
            "customerId": 21620,
            "userId": 19553,
            "domain": None,
            "widgets": [
                {
                    "showAs": "timeSeries",
                    "name": "CPU usage by instance",
                    "gridConfiguration": {
                        "col": 1,
                        "row": 1,
                        "size_x": 6,
                        "size_y": 6
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": 100
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "cloudProvider.id",
                            "propertyName": "k1"
                        },
                        {
                            "id": "aws.ec2.CPUUtilization",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "timeSeriesArea",
                    "name": "Zone aggregated network traffic",
                    "gridConfiguration": {
                        "col": 7,
                        "row": 1,
                        "size_x": 6,
                        "size_y": 6
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "aws.ec2.NetworkIn",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "sum"
                        },
                        {
                            "id": "aws.ec2.NetworkOut",
                            "propertyName": "v1",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "sum"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "timeSeries",
                    "name": "RDS CPU Usage Over Time",
                    "gridConfiguration": {
                        "col": 1,
                        "row": 7,
                        "size_x": 6,
                        "size_y": 5
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "logarithmic32",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "aws.rds.CPUUtilization",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "summary",
                    "name": "RDS-Freeable Memory Over Time",
                    "gridConfiguration": {
                        "col": 7,
                        "row": 7,
                        "size_x": 2,
                        "size_y": 2
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "aws.rds.FreeableMemory",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None,
                    "colorCoding": None
                },
                {
                    "showAs": "timeSeries",
                    "name": "RDS-Network Traffic Over Time",
                    "gridConfiguration": {
                        "col": 1,
                        "row": 12,
                        "size_x": 6,
                        "size_y": 5
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "aws.rds.NetworkReceiveThroughput",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        },
                        {
                            "id": "aws.rds.NetworkTransmitThroughput",
                            "propertyName": "v1",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "timeSeries",
                    "name": "RDS-Connections Over Time",
                    "gridConfiguration": {
                        "col": 7,
                        "row": 9,
                        "size_x": 6,
                        "size_y": 3
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "aws.rds.DatabaseConnections",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "summary",
                    "name": "RDS-Free Disk Space Over Time",
                    "gridConfiguration": {
                        "col": 11,
                        "row": 7,
                        "size_x": 2,
                        "size_y": 2
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "aws.rds.FreeStorageSpace",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None,
                    "colorCoding": None
                },
                {
                    "showAs": "timeSeries",
                    "name": "RDS-Disk Throughput Over Time",
                    "gridConfiguration": {
                        "col": 7,
                        "row": 12,
                        "size_x": 6,
                        "size_y": 5
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "timestamp",
                            "propertyName": "k0"
                        },
                        {
                            "id": "aws.rds.ReadThroughput",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        },
                        {
                            "id": "aws.rds.WriteThroughput",
                            "propertyName": "v1",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None
                },
                {
                    "showAs": "summary",
                    "name": "EC2 Credit Balance",
                    "gridConfiguration": {
                        "col": 9,
                        "row": 7,
                        "size_x": 2,
                        "size_y": 2
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": False,
                    "metrics": [
                        {
                            "id": "aws.ec2.CPUCreditBalance",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "compareToConfig": None,
                    "colorCoding": None
                },
                {
                    "showAs": "map",
                    "name": "Network Traffic",
                    "gridConfiguration": {
                        "col": 1,
                        "row": 17,
                        "size_x": 12,
                        "size_y": 6
                    },
                    "customDisplayOptions": {
                        "valueLimit": {
                            "count": 10,
                            "direction": "desc"
                        },
                        "histogram": {
                            "numberOfBuckets": 10
                        },
                        "yAxisScale": "linear",
                        "yAxisLeftDomain": {
                            "from": 0,
                            "to": None
                        },
                        "yAxisRightDomain": {
                            "from": 0,
                            "to": None
                        },
                        "xAxis": {
                            "from": 0,
                            "to": None
                        }
                    },
                    "scope": None,
                    "overrideScope": True,
                    "metrics": [
                        {
                            "id": "net.bytes.total",
                            "propertyName": "v0",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "avg"
                        }
                    ],
                    "limitToScope": False,
                    "linkMetrics": [
                        {
                            "id": "net.bytes.total",
                            "timeAggregation": "timeAvg",
                            "groupAggregation": "sum"
                        }
                    ],
                    "groupingLabelIds": [
                        {
                            "id": "cloudProvider.tag.aws:cloudformation:stack-id"
                        },
                        {
                            "id": "cloudProvider.tag.aws:cloudformation:logical-id"
                        }
                    ]
                }
            ],
            "scopeExpressionList": None,
            "eventsOverlaySettings": {
                "showNotificationsEnabled": True,
                "filterNotificationsScopeFilter": True,
                "filterNotificationsUserInputFilter": "",
                "eventOverlayLimit": 1000,
                "filterNotificationsTypeFilter": "all",
                "filterNotificationsStateFilter": "all",
                "filterNotificationsSeverityFilter": "all",
                "filterNotificationsResolvedFilter": "all"
            },
            "version": 1,
            "shared": False,
            "schema": 2,
            "publicToken": None,
            "username": "email@sysdig.com",
            "teamId": 17009,
            "createdOn": 1586272227000,
            "autoCreated": False,
            "modifiedOn": 1586272227000,
            "favorite": False,
            "name": DASHBOARD_NAME,
            "id": DASHBOARD_ID,
            "public": False
        }

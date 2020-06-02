from doublex import ANY_ARG, Spy, when
from doublex_expects import have_been_called_with, any_arg
from expects import *
from mamba import before, context, description, it
from sdcclient import SdMonitorClient

from sdccli.usecases import dashboard as use_case
from sdccli.usecases.dashboard import PanelBuilder

DASHBOARD_ID = 159639
DASHBOARD_NAME = "AWS EC2 CloudWatch"

with description(use_case.Dashboard) as self:
    with before.each:
        self.saved_test_dashboard = self.test_dashboard()
        self.monitor_client = Spy(SdMonitorClient)
        when(self.monitor_client).get_dashboards().returns(
            [True, {"dashboards": [self.saved_test_dashboard]}]
        )
        when(self.monitor_client).find_dashboard_by(ANY_ARG).returns(
            (True, [])
        )
        when(self.monitor_client).find_dashboard_by(DASHBOARD_NAME).returns(
            (True, [{"dashboard": self.saved_test_dashboard}])
        )
        when(self.monitor_client).create_dashboard_with_configuration(ANY_ARG).returns(
            (False, "Invalid dashboard spec")
        )
        when(self.monitor_client).create_dashboard_with_configuration(self.saved_test_dashboard).returns(
            (True, self.saved_test_dashboard)
        )
        when(self.monitor_client).add_dashboard_panel(ANY_ARG).returns(
            (True, {"dashboard": self.saved_test_dashboard})
        )
        when(self.monitor_client).add_dashboard_panel({}, ANY_ARG).returns(
            (False, "Error adding panel to dashboard")
        )

        self.monitor_client2 = SdMonitorClient()  # TODO: REMOVE

    with context("when a dashboard exists"):
        with it("can retrieve the existing dashboard by id"):
            dashboard = use_case.get_dashboard_by_id_or_name(self.monitor_client, DASHBOARD_ID)

            expect(dashboard).to(equal(self.saved_test_dashboard))

        with it("can retrieve the existing dashboard by name"):
            dashboard = use_case.get_dashboard_by_id_or_name(self.monitor_client, DASHBOARD_NAME)

            expect(dashboard).to(equal(self.saved_test_dashboard))

        with it("can list the existing dashboards"):
            res = use_case.list_dashboards(self.monitor_client)

            expect(res).to(have_length(1))
            expect(res[0]).to(equal(self.saved_test_dashboard))

        with it("creates a dashboard from json"):
            result = use_case.add_json_dashboard(self.monitor_client, self.saved_test_dashboard)

            expect(result).to(equal(f"Created dashboard {DASHBOARD_NAME}"))

        with it("creates a dashboard from json list"):
            result = use_case.add_json_dashboard(self.monitor_client,
                                                 [self.saved_test_dashboard, self.saved_test_dashboard])

            expect(result).to(equal(f"Created dashboard {DASHBOARD_NAME}\nCreated dashboard {DASHBOARD_NAME}\n"))

        with it("creates a panel for a dashboard"):
            panel = PanelBuilder() \
                .with_metric("aws.rds.NetworkReceiveThroughput") \
                .with_metric("aws.rds.NetworkTransmitThroughput") \
                .with_type("timeSeries") \
                .with_name("Traffic Over Time") \
                .with_layout(col=1, row=12, width=6, height=5) \
                .with_limit(10) \
                .build()

            expect(panel.name).to(equal("Traffic Over Time"))
            expect(panel.metrics).to(contain({"id": "aws.rds.NetworkReceiveThroughput"}))
            expect(panel.metrics).to(contain({"id": "aws.rds.NetworkTransmitThroughput"}))
            expect(panel.type).to(equal("timeSeries"))
            expect(panel.scope).to(be_none)
            expect(panel.limit).to(equal(10))
            expect(panel.sort).to(equal("desc"))
            expect(panel.layout_dict).to(have_keys({"col": 1, "row": 12, "size_x": 6, "size_y": 5}))

        with it("adds a panel to a dashboard"):
            panel = PanelBuilder().build()

            res = use_case.add_panel_to_dashboard(self.monitor_client, self.saved_test_dashboard, panel)

            expect(res).to(equal(self.test_dashboard()))

        with context("but the user specifies incorrect parameters"):
            with it("cannot retrieve a dashboard by incorrect id"):
                invalid_id = 0
                expect(lambda: use_case.get_dashboard_by_id_or_name(self.monitor_client, invalid_id)).to(
                    raise_error(Exception, "no dashboard with id 0")
                )

            with it("cannot retrieve a dashboard by incorrect name"):
                expect(lambda: use_case.get_dashboard_by_id_or_name(self.monitor_client, "invalid_name")).to(
                    raise_error(Exception, "no dashboard with name 'invalid_name' found")
                )

            with it("cannot create a dashboard from invalid json"):
                expect(lambda: use_case.add_json_dashboard(self.monitor_client, self.test_dashboard())).to(
                    raise_error(Exception, f"Error creating the dashboard {DASHBOARD_NAME}: Invalid dashboard spec")
                )
                expect(lambda: use_case.add_json_dashboard(self.monitor_client, {})).to(
                    raise_error(KeyError, "name")
                )
                expect(lambda: use_case.add_json_dashboard(self.monitor_client, "")).to(
                    raise_error(Exception, "Unsupported JSON format")
                )

            with it("cannot create a panel"):
                invalid_limit = 11
                expect(lambda: PanelBuilder().with_limit(invalid_limit).build()).to(
                    raise_error(Exception, f"invalid limit {invalid_limit} higher than the max of 10, "
                                           f"could cause rendering problems")
                )
                invalid_type = "invalid_type"
                expect(lambda: PanelBuilder().with_type(invalid_type).build()).to(
                    raise_error(Exception, f"invalid type {invalid_type}, must be one of "
                                           f"['timeSeries', 'top', 'number']")
                )

                invalid_name = ''
                expect(lambda: PanelBuilder().with_name(invalid_name).build()).to(
                    raise_error(Exception, f"name invalid or empty: '{invalid_name}'")
                )

                invalid_name = None
                expect(lambda: PanelBuilder().with_name(invalid_name).build()).to(
                    raise_error(Exception, f"name invalid or empty: '{invalid_name}'")
                )

                invalid_name = ["foo"]
                expect(lambda: PanelBuilder().with_name(invalid_name).build()).to(
                    raise_error(Exception, f"name invalid or empty: '{invalid_name}'")
                )

                invalid_name = {"foo": "bar"}
                expect(lambda: PanelBuilder().with_name(invalid_name).build()).to(
                    raise_error(Exception, f"name invalid or empty: '{invalid_name}'")
                )

            with it("cannot add a panel to a dashboard"):
                panel = PanelBuilder().build()
                expect(lambda: use_case.add_panel_to_dashboard(self.monitor_client, {}, panel)).to(
                    raise_error(Exception, "Error adding panel to dashboard")
                )


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

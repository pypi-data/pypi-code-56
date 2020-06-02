from doublex import Spy, when
from doublex_expects import *
from expects import *
from mamba import *
from sdcclient import SdMonitorClient

from sdccli.usecases import alert as use_case

ALERT_ID = 1783267
ALERT_NAME = "[sdc-cli-test] Name"

with description(sdccli.usecases.alert) as self:
    with before.each:
        self.monitor = Spy(SdMonitorClient)
        when(self.monitor).get_alerts().returns([True, {'alerts': [self.test_alert()]}])

    with context('when the alert already exists'):
        with it('retrieves the alert using its id'):
            res = use_case.alert_get(self.monitor, ALERT_ID)

            expect(res["id"]).to(equal(ALERT_ID))

        with it('retrieves the alert using its name'):
            res = use_case.alert_get(self.monitor, ALERT_NAME)

            expect(res).to(have_keys(name=ALERT_NAME))

        with it('updates the alert'):
            alert = self.test_alert()
            new_name = "[sdc-cli-test] Updated name"
            alert["name"] = new_name

            when(self.monitor).update_alert(alert).returns([True, {"alert": alert}])

            res = use_case.alert_update(self.monitor, alert)

            expect(self.monitor.update_alert).to(have_been_called_with(alert))
            expect(res).to(have_keys(name=new_name))

        with it('lists all the alerts'):
            when(self.monitor).get_alerts().returns([True, {"alerts": [self.test_alert()]}])

            res = use_case.alert_list(self.monitor)

            expect(res).to(contain(have_keys(name='[sdc-cli-test] Name')))

    with context("when the alert does not exist"):
        with it('creates an alert with default parameters'):
            when(self.monitor).create_alert(
                name=ALERT_NAME,
                description="alert_description",
                severity=4,
                for_atleast_s=600,
                condition="avg(avg(cpu.used.percent)) > 50",
                enabled=True,
                segmentby=["kubernetes.cluster.name"],
                segment_condition="ANY",
                user_filter="",
                notify=None,
                annotations={}
            ).returns([True, {"alert": self.test_alert()}])

            res = use_case.alert_add(
                self.monitor,
                name=ALERT_NAME,
                description="alert_description",
                severity=4,
                atleast=600,
                condition="avg(avg(cpu.used.percent)) > 50",
                disable=False,
                segment=["kubernetes.cluster.name"],
                segment_condition="ANY",
                user_filter="",
                notify=None,
                annotation={}
            )

            expect(res).to(equal(self.test_alert()))

        with it('can create alert from json'):
            alert_to_create = self.test_alert()
            when(self.monitor).create_alert(alert_obj=alert_to_create).returns([True, {"alert": alert_to_create}])

            res = use_case.alert_add_json(self.monitor, alert_to_create)

            expect(res).to(equal(alert_to_create))

        with context("and an error happens"):
            with it('cannot retrieve the alert using its id'):
                invalid_alert_id = 0

                expect(lambda: use_case.alert_get(self.monitor, invalid_alert_id)).to(
                    raise_error(Exception, f"no alert with id {invalid_alert_id}")
                )

            with it('cannot retrieve the alert using its name'):
                invalid_alert_name = "unexisting_alert"

                expect(lambda: use_case.alert_get(self.monitor, invalid_alert_name)).to(
                    raise_error(Exception, f"no alert with name {invalid_alert_name}")
                )

            with it('cannot update the alert'):
                invalid_alert_id = 0
                new_name = "[sdc-cli-test] Updated name"

                alert = self.test_alert()
                alert["id"] = invalid_alert_id
                alert["name"] = new_name

                when(self.monitor).update_alert(alert).returns((False,
                                                                'Sorry, something really bad happened with your request '
                                                                '(traceId: 34edff13d4d18e98).: system.error'))

                expect(lambda: use_case.alert_update(self.monitor, alert)).to(
                    raise_error(Exception, contain("Sorry, something really bad happened with your request"))
                )


    def test_alert(self):
        return {'id': ALERT_ID,
                'version': 1,
                'createdOn': 1588692353000,
                'modifiedOn': 1588692353000,
                'type': 'MANUAL',
                'name': '[sdc-cli-test] Name',
                'description': 'alert_description',
                'enabled': True,
                'filter': '',
                'severity': 4,
                'timespan': 600000000,
                'customNotification': {
                    'titleTemplate': '{{__alert_name__}} is {{__alert_status__}} on kubernetes.cluster.name = {{kubernetes.cluster.name}}',
                    'useNewTemplate': False
                },
                'notificationCount': 0,
                'teamId': 17009,
                'autoCreated': False,
                'rateOfChange': False,
                'reNotifyMinutes': 30,
                'reNotify': False,
                'invalidMetrics': [],
                'valid': True,
                'severityLabel': 'LOW',
                'segmentBy': ['kubernetes.cluster.name'],
                'segmentCondition': {'type': 'ANY'},
                'condition': 'avg(avg(cpu.used.percent)) > 50'
                }

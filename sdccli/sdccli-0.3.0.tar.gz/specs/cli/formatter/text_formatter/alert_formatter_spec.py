import contextlib
from io import StringIO

from expects import expect, equal
from mamba import description, context, it

from sdccli.cli.formatter import text_formatter

ALERT_ID = 1783267
ALERT_NAME = '[sdc-cli-test] Name'

with description(text_formatter.alert) as self:
    with context('when we are using the default formatter to present alerts'):
        with it('prints an element correctly'):
            with contextlib.redirect_stdout(StringIO()) as out:
                text_formatter.alert.format_alert(self.test_alert())
            expect(out.getvalue()).to(equal(self.formatted_test_alert()))

        with it("prints the list correctly"):
            with contextlib.redirect_stdout(StringIO()) as out:
                text_formatter.alert.format_alert_list([self.test_alert()])
            expect(out.getvalue()).to(equal(self.formatted_test_alert_list()))


    def formatted_test_alert(self):
        return ('id:                       1783267\n'
                'name:                     [sdc-cli-test] Name\n'
                'description:              alert_description\n'
                'type:                     MANUAL\n'
                'enabled:                  True\n'
                'severityLabel:            LOW\n'
                'segmentBy:                [\'kubernetes.cluster.name\']\n'
                'segmentCondition:\n'
                '    {\n'
                '      "type": "ANY"\n'
                '    }\n'
                'condition:                avg(avg(cpu.used.percent)) > 50\n'
                'timespan:                 600000000\n')


    def formatted_test_alert_list(self):
        return ('id             name                       type          enabled        severityLabel        \n'
                '1783267        [sdc-cli-test] Name        MANUAL        True           LOW                  \n')


    def test_alert(self):
        return {'id': ALERT_ID,
                'version': 1,
                'createdOn': 1588692353000,
                'modifiedOn': 1588692353000,
                'type': 'MANUAL',
                'name': ALERT_NAME,
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

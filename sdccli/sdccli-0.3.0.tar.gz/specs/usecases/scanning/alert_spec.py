from mamba import *
from expects import *
from doublex import *
from doublex_expects import *
from sdcclient import SdScanningClient

from sdccli.usecases.scanning import alert as use_case

ALERT_ID = "alert_1c5K1M4J78JYFuffSQNYxAZcttX"

with description("scanning_alert") as self:
    with before.each:
        self.scanning = Spy(SdScanningClient)
        when(self.scanning).get_alert(ANY_ARG).returns(
            (False, "Alert does not exist")
        )
        when(self.scanning).get_alert(ALERT_ID).returns(
            (True, self.test_scanning_alert())
        )
        when(self.scanning).list_alerts(ANY_ARG).returns(
            (True, {"alerts": [self.test_scanning_alert()]})
        )

    with context("when a scanning alert exists"):
        with it("is able to retrieve it"):
            res = use_case.get_alert_by_id(self.scanning, ALERT_ID)

            expect(res).to(equal(self.test_scanning_alert()))

        with it("is able to list it"):
            res = use_case.list_scanning_alerts(self.scanning)

            expect(res).to(contain(self.test_scanning_alert()))

        with it("is able to update it"):
            when(self.scanning).update_alert(ALERT_ID, self.test_scanning_alert()).returns(
                (True, self.test_scanning_alert())
            )

            res = use_case.update_scanning_alert(self.scanning, ALERT_ID, self.test_scanning_alert())

            expect(res).to(equal(self.test_scanning_alert()))

        with it("is able to remove it"):
            when(self.scanning).delete_alert(ALERT_ID).returns(
                (True, f"Removed alert ${ALERT_ID}")
            )

            expect(lambda: use_case.delete_scanning_alert(self.scanning, ALERT_ID)).to_not(raise_error(Exception))

    with context("when a scanning alert does not exist"):
        with it("throws an error"):
            non_existing_alert = "non_existing_alert"
            expect(lambda: use_case.get_alert_by_id(self.scanning, non_existing_alert)).to(
                raise_error(Exception, "Alert does not exist")
            )

        with it("is able to create it"):
            when(self.scanning).add_alert(ANY_ARG).returns(
                (True, self.test_scanning_alert())
            )
            res = use_case.add_scanning_alert(self.scanning,
                                              name="TestAlertName",
                                              description="TestAlertDescription",
                                              scope=None,
                                              unscanned=True,
                                              failed=False,
                                              enabled=True,
                                              notification_channels=[29198])

            expect(self.scanning.add_alert).to(have_been_called_with(
                name="TestAlertName",
                description="TestAlertDescription",
                enabled=True,
                scope=None,
                triggers={
                    'unscanned': True,
                    'failed': False
                },
                notification_channels=[29198]
            ))
            expect(res).to(equal(self.test_scanning_alert()))

        with it("cannot update it"):
            when(self.scanning).update_alert(ALERT_ID, self.test_scanning_alert()).returns(
                (False, f"Alert with ID {ALERT_ID} not found")
            )

            expect(lambda: use_case.update_scanning_alert(self.scanning, ALERT_ID, self.test_scanning_alert())).to(
                raise_error(Exception, f"Alert with ID {ALERT_ID} not found")
            )

        with it("cannot remove it"):
            when(self.scanning).delete_alert(ALERT_ID).returns(
                (False, f"Alert with ID {ALERT_ID} not found")
            )

            expect(lambda: use_case.delete_scanning_alert(self.scanning, ALERT_ID)).to(
                raise_error(Exception, f"Alert with ID {ALERT_ID} not found")
            )


    def test_scanning_alert(self):
        return {
            "createdAt": "2020-05-18T14:39:57Z",
            "updatedAt": "2020-05-18T14:40:33Z",
            "customerId": 21620,
            "teamId": 17616,
            "alertId": ALERT_ID,
            "enabled": True,
            "type": "runtime",
            "name": "TestAlertName",
            "description": "TestAlertDescription",
            "scope": "",
            "repositories": [],
            "triggers": {
                "unscanned": True,
                "analysis_update": False,
                "vuln_update": True,
                "policy_eval": True,
                "failed": False
            },
            "autoscan": True,
            "onlyPassFail": True,
            "skipEventSend": False,
            "notificationChannelIds": [
                29198
            ]
        }

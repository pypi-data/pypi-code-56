# -*- coding: utf-8 -*-
"""
Testing modify expert bot.
"""

import unittest

from pkg_resources import resource_filename

import intelmq.lib.test as test
from intelmq.lib.utils import load_configuration
from intelmq.bots.experts.modify.expert import ModifyExpertBot, modify_expert_convert_config

EVENT_TEMPL = {"__type": "Event",
               "feed.name": "Spamhaus Cert",
               "feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                           "<CERTNAME>&key=<APIKEY>",
               "classification.taxonomy": "malicious code",
               "classification.type": "infected-system",
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
INPUT = [{'feed.name': 'Abuse.ch',
          'feed.url': 'https://feodotracker.abuse.ch/blocklist/?download=domainblocklist'},
         {'malware.name': 'foobar', 'feed.name': 'Other Feed'},
         {'source.port': 80, 'malware.name': 'zeus'},
         {'malware.name': 'xcodeghost'},
         {'malware.name': 'securityscorecard-someexample-value'},
         {'malware.name': 'anyvalue'},  # 5
         {},
         {'source.tor_node': True},
         {'source.tor_node': False},
         {},
         {'feed.accuracy': 5.22},  # 10
         {'feed.accuracy': 100},
         {'comment': 'integer value'},
         ]
OUTPUT = [{'classification.identifier': 'feodo'},
          {'classification.identifier': 'foobar'},
          {'protocol.transport': 'tcp', 'protocol.application': 'http',
           'classification.identifier': 'zeus'},
          {'classification.identifier': 'xcodeghost'},
          {'classification.identifier': 'someexample-value'},
          {'classification.identifier': 'anyvalue'},  # 5
          {'classification.type': 'vulnerable service'},
          {'event_description.text': 'This is a TOR node.'},
          {'event_description.text': 'This is not a TOR node.'},
          {'event_description.text': 'We don\'t know if this is a TOR node.'},
          {'event_description.text': 'Accuracy is 10% or lower.'},  # 10
          {'event_description.text': 'Accuracy is the highest.'},
          {'extra.test': 1, 'event_description.text': 'We don\'t know if this is a TOR node.'},
          ]
for index in range(len(INPUT)):
    copy1 = EVENT_TEMPL.copy()
    copy2 = EVENT_TEMPL.copy()
    copy1.update(INPUT[index])
    copy2.update(INPUT[index])
    copy2.update(OUTPUT[index])
    INPUT[index] = copy1
    OUTPUT[index] = copy2


class TestModifyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ModifyExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ModifyExpertBot
        config_path = resource_filename('intelmq',
                                        'bots/experts/modify/examples/default.conf')
        cls.sysconfig = {'configuration_path': config_path
                         }

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT[:6]
        self.allowed_warning_count = 1
        self.run_bot(iterations=6)

        for position, event_out in enumerate(OUTPUT[:6]):
            self.assertMessageEqual(position, event_out)

    def test_conversion(self):
        """ Test if the conversion from old dict-based config to new list based is correct. """
        old_path = resource_filename('intelmq',
                                     'tests/bots/experts/modify/old_format.conf')
        old_config = load_configuration(old_path)
        new_path = resource_filename('intelmq',
                                     'tests/bots/experts/modify/new_format.conf')
        new_config = load_configuration(new_path)
        self.assertDictEqual(modify_expert_convert_config(old_config)[0],
                             new_config[0])

    def test_types(self):
        """
        boolean, int etc
        """
        config_path = resource_filename('intelmq',
                                        'tests/bots/experts/modify/types.conf')
        parameters = {'configuration_path': config_path,
                      'overwrite': True}
        self.input_message = INPUT[7:13]
        self.run_bot(parameters=parameters,
                     iterations=len(INPUT[7:13]))
        for position, event_out in enumerate(OUTPUT[7:13]):
            self.assertMessageEqual(position, event_out)

    def test_overwrite(self):
        """
        test if bot overwrites by default
        """
        config_path = resource_filename('intelmq',
                                        'tests/bots/experts/modify/overwrite.conf')
        self.input_message = INPUT[6]
        self.allowed_warning_count = 1
        self.run_bot(parameters={'configuration_path': config_path})
        self.assertMessageEqual(0, OUTPUT[6])

    def test_overwrite_not(self):
        """
        test if bot does not overwrites if parameter is set
        """
        config_path = resource_filename('intelmq',
                                        'tests/bots/experts/modify/overwrite.conf')
        self.input_message = EVENT_TEMPL
        self.run_bot(parameters={'configuration_path': config_path,
                                 'overwrite': False})
        self.assertMessageEqual(0, EVENT_TEMPL)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

#CHIPSEC: Platform Security Assessment Framework
#Copyright (c) 2018-2020, Intel Corporation
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; Version 2.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#Contact information:
#chipsec@intel.com
#


from chipsec.module_common import BaseModule, ModuleResult, MTAG_HWCONFIG

TAGS = [MTAG_HWCONFIG]

class ia_untrusted(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)

    def is_supported(self):
        if self.cs.is_register_defined('MSR_BIOS_DONE') and self.cs.register_has_field('MSR_BIOS_DONE', 'IA_UNTRUSTED'):
            return True
        self.res = ModuleResult.NOTAPPLICABLE
        return False

    def run(self, module_argv):
        self.logger.start_test('IA_UNTRUSTED Check')
        self.logger.log('[*] Check that untrusted mode has been set.')
        ia_untrusted = self.cs.read_register_field('MSR_BIOS_DONE', 'IA_UNTRUSTED')
        if ia_untrusted == 0:
            self.res = ModuleResult.FAILED
            self.logger.log_failed_check('IA_UNTRUSTED not set.')
        else:
            self.logger.log_passed_check('IA_UNTRUSTED set.')
            self.res = ModuleResult.PASSED
        return self.res

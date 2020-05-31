import logging
import datetime
import time

from Utils.Subprocess import call, check_call
from Tc.Tbf import TbfCollection, Tbf
from Tc.Filter import Filter, TcFilter
from Tc.Netem import NetemCollection, Duplicate, Delay, Loss, Reorder, Corrupt,Rate


class TcWrapper(object):
    """Wrapper around tc module

    Class functions as a wrapper before all tc related
    classes are called, handles their parameters and
    does basic initialization along with teardown

    """
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        nic = self.nic
        self.nic = 'ifb1' if not self.direction == "Egress" else nic
        self.real_nic = nic

    def tbf(self, operation):
        """Control of tbf

        :param operation type of operation to be executed

        Function hands over appropriate parameters to tbf,
        creates the command and applies it
        """
        tbf = Tbf(self.limit,
                  self.burst,
                  self.latency)

        tbf_collection = TbfCollection(self.nic)
        tbf_collection.append(tbf)
        tbf_collection.apply_cmd(operation=operation)

    def netem(self, operation):
        """Control of netem

        :param operation type of operation to be executed

        Function hands over appropriate parameters to netem,
        creates the command and applies it
        """
        loss = Loss(self.loss_ratio,
                    self.loss_corr)

        dupl = Duplicate(self.dupl_ratio,
                         self.dupl_corr)

        delay = Delay(self.delay,
                      self.jitter,
                      self.delay_jitter_corr)

        reorder = Reorder(self.reorder_ratio,
                          self.reorder_corr)

        corrupt = Corrupt(self.corrupt_ratio)

        rate = Rate(self.limit,
                    self.overhead)

        netem_collection = NetemCollection(self.nic)
        netem_collection.extend([loss, dupl, delay, reorder, corrupt, rate])
        netem_collection.apply_cmd(operation=operation)

    def initialize(self):
        """Initialization of qdisc scheduler and filters

        Function decides what kind of qdiscs are required based on
        the direction of the emulation. Inclusion and exclusion
        filters are applied on top of the root qdisc to create
        a tree hierarchy

        """
        logging.info("Initializing and cleaning up previous configuration.")

        if not self.direction == "Egress":
            self.ingress_setup()

        call(f"tc qdisc del root dev {self.nic} ")
        check_call(f"tc qdisc add dev {self.nic} root handle 1: prio")

        exclude_filters, exclude_filters_ipv6 = Filter.generate_filters(self.exclude)
        TcFilter(exclude_filters, exclude_filters_ipv6, self.nic, "exclude")

        include_filters, include_filters_ipv6 = Filter.generate_filters(self.include)
        TcFilter(include_filters, include_filters_ipv6, self.nic, "include")

    def teardown(self):
        """Teardown of existing tc setup

        Function based on the direction of the emulation deletes
        approriate qdisc, filters and interfaces to
        end the emulation
        """
        if not self.direction == "Egress":
            call(f"tc filter del dev {self.real_nic} parent ffff: protocol ip prio 1")
            call(f"tc qdisc del dev {self.real_nic} ingress")
            call("ip link set dev ifb0 down")

        call(f"tc qdisc del root dev {self.nic}")
        logging.info("Network impairment emulation teardown complete.")

    def ingress_setup(self):
        """Function to setup the ingress datapath

        If ingress parameter is specified ifb module
        is loaded and ingress qdisc of real interface
        is replaced with ifb to be able to perform
        all tc related operations
        """
        check_call("modprobe ifb")
        check_call(f"ip link set dev {self.nic} up")
        call(f"tc qdisc del dev {self.real_nic} ingress ")
        check_call(f"tc qdisc replace dev {self.real_nic} ingress")
        check_call(f"tc filter replace dev {self.real_nic} parent ffff: protocol "
                   f"ip prio 1 u32 match u32 0 0 flowid 1:1 action mirred egress "
                   f"redirect dev {self.nic}")

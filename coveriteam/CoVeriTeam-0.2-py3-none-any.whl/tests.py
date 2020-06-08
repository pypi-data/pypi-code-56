# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.actors.misc import TestCriterionInstrumentor
from coveriteam.actors.testers import ProgramTester
from coveriteam.actors.validators import ProgramValidator
from coveriteam.actors.verifiers import ProgramVerifier
from coveriteam.language.artifact import (
    TestGoal,
    CProgram,
    ReachSafety,
    MemSafety,
    Termination,
    NoOverflow,
    BranchCoverage,
)
import logging
from coveriteam.example_compositions import (
    validated_verifier,
    metaval_prototype,
    conditional_tester,
    verifier_based_tester,
    conditional_tester_verifier_based,
    atva_paper_fig_14,
)
import coveriteam.util as util
import os


def test_data_unreach_call_false():
    input_program_path = util.INPUT_FILE_DIR + "c/Problem02_label16.c"
    property_path = util.INPUT_FILE_DIR + "specifications/unreach-call.prp"

    return CProgram(input_program_path), ReachSafety(property_path)


def test_data_unreach_call_true():
    input_program_path = util.INPUT_FILE_DIR + "c/Problem01_label00.c"
    property_path = util.INPUT_FILE_DIR + "specifications/unreach-call.prp"

    return CProgram(input_program_path), ReachSafety(property_path)


def test_data_termination_false():
    input_program_path = util.INPUT_FILE_DIR + "c/Madrid.c"
    property_path = util.INPUT_FILE_DIR + "specifications/termination.prp"

    return CProgram(input_program_path), Termination(property_path)


def test_data_memsafety_false():
    input_program_path = util.INPUT_FILE_DIR + "c/cstrcat_unsafe.c"
    property_path = util.INPUT_FILE_DIR + "specifications/valid-memsafety.prp"

    return CProgram(input_program_path), MemSafety(property_path)


def test_data_nooverflow_false():
    input_program_path = util.INPUT_FILE_DIR + "c/AdditionIntMax.i"
    property_path = util.INPUT_FILE_DIR + "specifications/no-overflow.prp"

    return CProgram(input_program_path), NoOverflow(property_path)


def test_data_nooverflow_true():
    input_program_path = util.INPUT_FILE_DIR + "c/ConversionToSignedInt.i"
    property_path = util.INPUT_FILE_DIR + "specifications/no-overflow.prp"

    return CProgram(input_program_path), NoOverflow(property_path)


def uc_validated_verifier_cpachecker_based(cprogram, spec):
    logging.info("Executing CPAchecker based validated verifier:")

    vv = validated_verifier(
        ProgramVerifier("config/cpa-seq.yml"),
        ProgramValidator("config/cpa-validate-violation-witnesses.yml"),
    )

    return vv.act(program=cprogram, spec=spec)


def uc_validated_verifier_ultimate_cpachecker(cprogram, spec):
    logging.info("Executing CPAchecker based validated verifier:")

    vv = validated_verifier(
        ProgramVerifier("config/uautomizer.yml"),
        ProgramValidator("config/cpa-validate-violation-witnesses.yml"),
    )

    return vv.act(program=cprogram, spec=spec)


def uc_validated_verifier_cpachecker_metaval(cprogram, spec):
    logging.info("Executing CPAchecker based validated verifier:")

    vv = validated_verifier(ProgramVerifier("config/cpa-seq.yml"), metaval_prototype())
    verdict, witness = vv.act(program=cprogram, spec=spec)

    return verdict, witness


def test_validated_verifier(ver, val):
    vv = validated_verifier(ver, val)
    cprogram, spec = test_data_unreach_call_false()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: False, Actual: {}".format(res["verdict"]))
    cprogram, spec = test_data_unreach_call_true()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: True, Actual: {}".format(res["verdict"]))


def test_validated_verifier_produce_xml(ver, val):
    vv = validated_verifier(ver, val)
    cprogram, spec = test_data_unreach_call_false()
    res = vv.act_and_save_xml(program=cprogram, spec=spec)
    print("Exected: False, Actual: {}".format(res["verdict"]))


def test_validated_verifier_metaval(ver):
    vv = validated_verifier(ver, metaval_prototype())
    print("Testing unreach call.......")
    cprogram, spec = test_data_unreach_call_false()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing unreach call.......")
    cprogram, spec = test_data_unreach_call_true()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: TRUE, Actual: {}".format(res["verdict"]))

    print("Testing overflow.......")
    cprogram, spec = test_data_nooverflow_false()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing overflow.......")
    cprogram, spec = test_data_nooverflow_true()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: TRUE, Actual: {}".format(res["verdict"]))

    print("Testing memory safety......")
    cprogram, spec = test_data_memsafety_false()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing Termination.......")
    cprogram, spec = test_data_termination_false()
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))


def test_verifier_based_tester(ver):
    print("...............Testing Verifier based tester")
    cprogram, spec = test_data_verifier_based_tester()
    verifier_based_tester(ver).act(program=cprogram, spec=spec)


def test_data_for_condtest():
    input_program_path = util.INPUT_FILE_DIR + "c/test.c"
    property_path = util.INPUT_FILE_DIR + "specifications/coverage-branches.prp"

    return CProgram(input_program_path), BranchCoverage(property_path)


def test_conditional_testing():
    print("...............Testing Conditional Tester with klee")
    cprogram, spec = test_data_for_condtest()
    ct = conditional_tester(ProgramTester("config/klee.yml"))
    instrumented_program = TestCriterionInstrumentor(
        "config/test-criterion-instrumentor.yml"
    ).act(program=cprogram, test_spec=spec)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(
        program=instrumented_program["program"],
        test_spec=spec,
        covered_goals=TestGoal(""),
    )


def test_data_verifier_based_tester():
    input_program_path = util.INPUT_FILE_DIR + "c/Problem01_label15.c"
    property_path = util.INPUT_FILE_DIR + "specifications/unreach-call.prp"

    return CProgram(input_program_path), ReachSafety(property_path)


def test_data_for_condtest_verifier_based():
    input_program_path = util.INPUT_FILE_DIR + "c/Problem01_label15.c"
    property_path = util.INPUT_FILE_DIR + "specifications/coverage-branches.prp"

    return CProgram(input_program_path), BranchCoverage(property_path)


def test_conditional_testing_verifier_based(ver):
    print("...............Testing Conditional Tester -- Verifier based")
    cprogram, spec = test_data_for_condtest_verifier_based()
    ct = conditional_tester_verifier_based(ver)
    instrumented_program = TestCriterionInstrumentor(
        "config/test-criterion-instrumentor.yml"
    ).act(program=cprogram, test_spec=spec)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(
        program=instrumented_program["program"],
        test_spec=spec,
        covered_goals=TestGoal(""),
    )


def test_atva_paper_fig_14(ver):
    print("...............Testing ATVA paper fig 14")
    cprogram, spec = test_data_for_condtest_verifier_based()
    ct = atva_paper_fig_14(ver)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(program=cprogram, test_spec=spec, covered_goals=TestGoal(""))


def test_all():
    test_validated_verifier(
        ProgramVerifier("config/cpa-seq.yml"),
        ProgramValidator("config/cpa-validate-violation-witnesses.yml"),
    )
    test_validated_verifier(
        ProgramVerifier("config/uautomizer.yml"),
        ProgramValidator("config/cpa-validate-violation-witnesses.yml"),
    )
    test_verifier_based_tester(ProgramVerifier("config/cpa-seq.yml"))
    test_validated_verifier_metaval(ProgramVerifier("config/cpa-seq.yml"))
    test_validated_verifier_metaval(ProgramVerifier("config/uautomizer.yml"))
    test_conditional_testing()
    test_conditional_testing_verifier_based(ProgramVerifier("config/cpa-seq.yml"))
    test_atva_paper_fig_14(ProgramVerifier("config/cpa-seq.yml"))


util.LOG_DIR = os.path.join(os.getcwd(), util.LOG_DIR)
DEBUG = None
FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

test_all()

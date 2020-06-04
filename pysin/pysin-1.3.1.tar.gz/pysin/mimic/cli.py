import pandas as pd
from sqlalchemy import create_engine

from .database_generator import DataBaseRandomGenerator
from .table import Table
from .attribute import Attribute
from .attribute_type import (
    FirstNameAttr,
    LastNameAttr,
    CityAttr,
    PostalCodeAttr,
    StreetAddressAttr,
    IntegerAttr,
    FloatAttr,
    RelativeFloatAttr,
    DigitIDAttr,
    DoubleDigitIDAttr,
    ComposedDigitIDAttr,
    EVDigitIDAttr,
    PhoneNumberAttr,
    DateAttr,
    FieldAttr,
)
from .mimic_preprocessing import MimicPreprocessing

import argparse


def scrap():
    parser = argparse.ArgumentParser(description="Scrap MIMIC-III data from alpha.physionet.org")
    parser.add_argument(
        "--dest",
        required=True,
        type=str,
        nargs=1,
        help="the destination path of the scrapped files",
    )
    args = parser.parse_args()

    mimic = MimicPreprocessing(args.dest[0])
    mimic.scraper(
        unused_tables=[
            "callout",
            "cptevents",
            "datetimeevents",
            "d_cpt",
            "inputevents_cv",
            "inputevents_mv",
            "noteevents",
            "outputevents",
            "procedureevents_mv",
        ]
    )


def generate():
    parser = argparse.ArgumentParser(description="Scrap MIMIC-III data from alpha.physionet.org")
    parser.add_argument(
        "--dest",
        required=True,
        type=str,
        nargs=1,
        help="the location of the scrapped files and where caching data will be stored",
    )
    parser.add_argument(
        "--db",
        required=True,
        type=str,
        nargs=1,
        help="the database connexion string (eg: postgresql://user:passsword@host/database)",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="should the mimic database be translated into french",
    )
    parser.add_argument(
        "--rows", required=True, type=int, nargs=1, help="The number of rows to generate",
    )

    args = parser.parse_args()

    mimic = MimicPreprocessing(args.dest[0])

    print("Connecting to postgres...")
    engine = create_engine(args.db[0])
    engine.connect()
    print("OK")

    attributes_dict, possible_values = mimic.infer_attributes()

    unused_attributes = [  # (table_name, attribute_name)
        ("d_items", "dbsource"),
        ("icustays", "dbsource"),
        ("icustays", "first_wardid"),
        ("icustays", "last_wardid"),
        ("transfers", "dbsource"),
        ("transfers", "prev_wardid"),
        ("transfers", "curr_wardid"),
    ]

    tables_to_add = [
        "hospit_services",
        "documents",
    ]

    attributes_to_add = {  # (table_name, Attribute)
        "patients": [
            ("first_name", Attribute(FirstNameAttr)),
            ("last_name", Attribute(LastNameAttr)),
            ("weight", Attribute(IntegerAttr, min_val=40, max_val=110)),
            ("height", Attribute(IntegerAttr, min_val=130, max_val=210)),
            ("street_address", Attribute(StreetAddressAttr)),
            ("postal_code", Attribute(PostalCodeAttr)),
            ("city", Attribute(CityAttr)),
        ],
        "documents": [
            ("date", Attribute(DateAttr)),
            ("type", Attribute(FieldAttr, possible_values=["prescription", "report"])),
            ("description", Attribute(FieldAttr, possible_values=["NONE"])),  # TODO
            (
                "patient_id",
                Attribute(FieldAttr, possible_values=possible_values["patients"]["subject_id"]),
            ),
            (
                "statut",
                Attribute(FieldAttr, possible_values=9 * ["TRUE"] + ["FALSE"]),
            ),  # TODO : BoolAttr
            ("document", Attribute(FieldAttr, possible_values=["NONE"]),),  # TODO : include PySin
            ("doc_id", Attribute(DigitIDAttr)),
            (
                "hadm_id",
                Attribute(FieldAttr, possible_values=possible_values["admissions"]["hadm_id"]),
            ),
        ],
        "hospit_services": [
            ("row_id", Attribute(DigitIDAttr)),
            (
                "careunit",
                Attribute(FieldAttr, possible_values=possible_values["services"]["curr_service"]),
            ),
        ],
    }

    attributes_to_translate = [  # (table_name, attr_name)
        ("admissions", "diagnosis"),
        ("drgcodes", "description"),
        ("d_icd_diagnoses", "short_title"),
        ("d_icd_diagnoses", "long_title"),
        ("d_icd_procedures", "short_title"),
        ("d_icd_procedures", "long_title"),
    ]

    tables = {}

    for table in tables_to_add:
        attributes_dict[table] = {}

    for curr_table in attributes_dict:
        curr_attributes = {}
        for attr, attr_class in attributes_dict[curr_table].items():
            if not (curr_table, attr) in unused_attributes:
                try:
                    attr_type, attr_params = attr_class.split("-", 1)
                except:
                    raise Exception(f"Wrong attribute class format : {attr_class}.")
                if attr_type == "digit_id":
                    curr_attributes[attr] = Attribute(DigitIDAttr, length=int(attr_params))
                elif attr_type == "date":
                    curr_attributes[attr] = Attribute(DateAttr)
                elif attr_type == "float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        FloatAttr, min_val=float(min_val), max_val=float(max_val)
                    )
                elif attr_type == "relative_float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        RelativeFloatAttr, min_val=float(min_val), max_val=float(max_val)
                    )
                elif attr_type == "double_digit_id":
                    curr_attributes[attr] = Attribute(DoubleDigitIDAttr, length=int(attr_params))
                elif attr_type == "composed_digit_id-":
                    curr_attributes[attr] = Attribute(ComposedDigitIDAttr)
                elif attr_type == "first_name":
                    curr_attributes[attr] = Attribute(FirstNameAttr)
                elif attr_type == "last_name":
                    curr_attributes[attr] = Attribute(LastNameAttr)
                elif attr_type == "city_name":
                    curr_attributes[attr] = Attribute(CityAttr)
                elif attr_type == "postal_code":
                    curr_attributes[attr] = Attribute(PostalCodeAttr)
                elif attr_type == "phone_number":
                    curr_attributes[attr] = Attribute(PhoneNumberAttr)
                elif attr_type == "ev_digit_id":
                    curr_attributes[attr] = Attribute(EVDigitIDAttr, digit_length=attr_params)
                elif attr_type == "field":
                    curr_attributes[attr] = Attribute(
                        FieldAttr, possible_values=possible_values[curr_table][attr_params]
                    )
                else:
                    raise Exception(f"Unknow attribute type : {attr_type}.")
                tables[curr_table.split(".")[0]] = Table(curr_attributes)
                try:
                    attr_type, attr_params = attr_class.split("-", 1)
                except:
                    raise Exception(f"Wrong attribute class format : {attr_class}.")
                if attr_type == "digit_id":
                    curr_attributes[attr] = Attribute(DigitIDAttr, length=int(attr_params))
                elif attr_type == "date":
                    curr_attributes[attr] = Attribute(DateAttr)
                elif attr_type == "float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        FloatAttr, min_val=float(min_val), max_val=float(max_val)
                    )
                elif attr_type == "relative_float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        RelativeFloatAttr, min_val=float(min_val), max_val=float(max_val)
                    )
                elif attr_type == "double_digit_id":
                    curr_attributes[attr] = Attribute(DoubleDigitIDAttr, length=int(attr_params))
                elif attr_type == "composed_digit_id-":
                    curr_attributes[attr] = Attribute(ComposedDigitIDAttr)
                elif attr_type == "first_name":
                    curr_attributes[attr] = Attribute(FirstNameAttr)
                elif attr_type == "last_name":
                    curr_attributes[attr] = Attribute(LastNameAttr)
                elif attr_type == "city_name":
                    curr_attributes[attr] = Attribute(CityAttr)
                elif attr_type == "postal_code":
                    curr_attributes[attr] = Attribute(PostalCodeAttr)
                elif attr_type == "phone_number":
                    curr_attributes[attr] = Attribute(PhoneNumberAttr)
                elif attr_type == "ev_digit_id":
                    curr_attributes[attr] = Attribute(EVDigitIDAttr, digit_length=attr_params)
                elif attr_type == "field":
                    curr_attributes[attr] = Attribute(
                        FieldAttr, possible_values=possible_values[curr_table][attr_params]
                    )
                else:
                    raise Exception(f"Unknow attribute type : {attr_type}.")
        if curr_table in attributes_to_add.keys():
            for attr_name, attr in attributes_to_add[curr_table]:
                curr_attributes[attr_name] = attr
        tables[curr_table.split(".")[0]] = Table(curr_attributes)

    print(f"Translation is {'enabled' if args.translate else 'disabled'}")
    for table_name, attr_name in attributes_to_translate:
        tables[table_name].attributes[attr_name].translation_required = args.translate

    relations = {
        "hadm_id": {
            "parents": [("admissions", "hadm_id"),],
            "children": [
                ("chartevents", "hadm_id", (1, 2)),
                # ('datetimeevents', 'hadm_id', (1, 2)),
                ("diagnoses_icd", "hadm_id", (1, 2)),
                ("drgcodes", "hadm_id", (1, 2)),
                ("icustays", "hadm_id", (1, 2)),
                ("procedures_icd", "hadm_id", (1, 2)),
                ("services", "hadm_id", (1, 2)),
                ("documents", "hadm_id", (1, 2)),
                ("transfers", "hadm_id", (1, 2)),
                ("prescriptions", "hadm_id", (1, 2)),
                ("labevents", "hadm_id", (1, 2)),
                ("microbiologyevents", "hadm_id", (1, 2)),
            ],
        },
        "subject_id": {
            "parents": [("patients", "subject_id"),],
            "children": [
                ("admissions", "subject_id", (1, 2)),
                ("chartevents", "subject_id", (1, 2)),
                # ('datetimeevents', 'subject_id', (1, 2)),
                ("diagnoses_icd", "subject_id", (1, 2)),
                ("drgcodes", "subject_id", (1, 2)),
                ("icustays", "subject_id", (1, 2)),
                ("procedures_icd", "subject_id", (1, 2)),
                ("services", "subject_id", (1, 2)),
                ("transfers", "subject_id", (1, 2)),
                ("prescriptions", "subject_id", (1, 2)),
                ("labevents", "subject_id", (1, 2)),
                ("microbiologyevents", "subject_id", (1, 2)),
                ("documents", "patient_id", (1, 2)),
            ],
        },
        "cgid": {
            "parents": [("caregivers", "cgid"),],
            "children": [
                ("chartevents", "cgid", (1, 2)),
                # ('datetimeevents', 'cgid', (1, 2)),
            ],
        },
        "icustay_id": {
            "parents": [("icustays", "icustay_id"),],
            "children": [
                ("chartevents", "icustay_id", (0, 2)),
                # ('datetimeevents', 'icustay_id', (1, 2)),
                ("transfers", "icustay_id", (1, 2)),
                ("prescriptions", "icustay_id", (1, 2)),
            ],
        },
        "itemid": {
            "parents": [("d_items", "itemid"),],
            "children": [
                ("chartevents", "itemid", (1, 2)),
                # ('datetimeevents', 'itemid', (1, 2)),
                ("labevents", "itemid", (1, 2)),
                ("microbiologyevents", "spec_itemid", (1, 2)),
                ("microbiologyevents", "org_itemid", (1, 2)),
                ("microbiologyevents", "ab_itemid", (1, 2)),
            ],
        },
        "icd9_code_diagnoses": {
            "parents": [("d_icd_diagnoses", "icd9_code"),],
            "children": [("diagnoses_icd", "icd9_code", (1, 2)),],
        },
        "icd9_code_procedures": {
            "parents": [("d_icd_procedures", "icd9_code"),],
            "children": [("procedures_icd", "icd9_code", (1, 2)),],
        },
        "service": {
            "parents": [("hospit_services", "careunit")],
            "children": [
                ("icustays", "first_careunit", (1, 2)),
                ("icustays", "last_careunit", (1, 2)),
                ("services", "prev_service", (1, 2)),
                ("services", "curr_service", (1, 2)),
                ("transfers", "prev_careunit", (1, 2)),
                ("transfers", "curr_careunit", (1, 2)),
            ],
        },
    }

    db_gen = DataBaseRandomGenerator(locale="fr_FR")  # or en_US

    for table_name, table in tables.items():
        db_gen.add_table(table_name, table)

    for relation_name, relation_dict in relations.items():
        db_gen.add_relation(relation_name, relation_dict)

    db_gen.random_generation(min_rows=args.rows[0])

    for table_name, table in tables.items():
        db_gen.tables[table_name].to_sql(table_name, engine)

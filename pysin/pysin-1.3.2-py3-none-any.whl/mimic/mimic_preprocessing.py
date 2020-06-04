import csv
import os
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from warnings import simplefilter

simplefilter("ignore")


class MimicPreprocessing:
    def __init__(self, dest_folder="data"):
        self.BASE_LINK = "https://alpha.physionet.org/files/mimiciii-demo/1.4/"
        self.dest_folder = dest_folder
        if not os.path.isdir(dest_folder):
            os.mkdir(dest_folder)
            os.mkdir(f"{dest_folder}/csv")
            os.mkdir(f"{dest_folder}/csv_unique_values")

    def scraper(self, unused_tables=[]):

        print("Starts scraping mimic...")

        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, log_path="/tmp/test")
        browser.get(self.BASE_LINK)

        filename_list = [x.text for x in browser.find_elements_by_xpath("//a[@href]")]

        i = 0
        for filename in filename_list:

            if not filename.split(".csv")[0].lower() in unused_tables:

                progress = (i + 1) / len(filename_list)
                print(
                    str("\r" + int(100 * progress) * "#" + int(100 * (1 - progress)) * "_"), end="",
                )

                if filename.endswith(".csv"):

                    browser.get(self.BASE_LINK + filename)
                    txt = browser.find_element_by_tag_name("pre").text

                    with open(f"{self.dest_folder}/csv/{filename.lower()}", "w+") as f:
                        f.write(txt)

                i += 1

        print("\nScrapping terminated !\n")

    def infer_attributes(self):

        print("Starts inferring attributes from mimic...")

        attribute_types_all_tables = {}

        possible_values_all_tables = {}

        targets = os.listdir(f"{self.dest_folder}/csv")

        f_count = 0

        for filename in targets:

            if filename.endswith(".csv"):
                progress = (f_count + 1) / len(targets)
                print(
                    int(100 * progress) * "■" + int(100 * (1 - progress)) * "_", end="\r",
                )

                attribute_types = {}
                possible_values = {}
                df = pd.read_csv(f"{self.dest_folder}/csv/{filename}").applymap(str)
                unique_values = {}
                attr_list = df.columns
                for attr in attr_list:
                    unique_values[attr] = df[attr].drop_duplicates().reset_index(drop=True)
                    try:
                        attr_values = unique_values[attr]
                        i = 0
                        while attr_values[i] == "":
                            i += 1
                        if (
                            False
                        ):  ############################################ TO FIX WHEN ATTRIBUTE TYPE DETECTION HAS BEEN SUFFICIENTLY IMPROVED (bad guessed type may lead to troubles with relations)
                            if re.match(r"^\d+$", attr_values[i]):
                                float_type = False
                                ev_digit_id_type = False
                                relative_float_type = False
                                length = len(attr_values[i])
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if not re.match(r"^\d+$", attr_values[j]):
                                            if re.match(r"^\d+\.\d+$", attr_values[j]):
                                                float_type = True
                                            elif re.match(r"^-\d+\.?\d*$", attr_values[j]):
                                                relative_float_type = True
                                            elif re.match(r"^[EV]?\d+$", attr_values[j]):
                                                ev_digit_id_type = True
                                            else:
                                                attribute_types[attr] = f"field-{attr}"
                                                possible_values[f"{attr}"] = attr_values
                                                is_field = True
                                                break
                                        else:
                                            length = max(length, len(attr_values[j]))
                                if not is_field:
                                    if ev_digit_id_type:
                                        attribute_types[attr] = f"ev_digit_id-"
                                    elif relative_float_type:
                                        min_value = min(
                                            [float(x) for x in attr_values if float(x) > 0]
                                        )
                                        max_value = max(
                                            [float(x) for x in attr_values if float(x) > 0]
                                        )
                                        attribute_types[
                                            attr
                                        ] = f"relative_float-{min_value}-{max_value}"
                                    elif float_type:
                                        min_value = min([float(x) for x in attr_values])
                                        max_value = max([float(x) for x in attr_values])
                                        attribute_types[attr] = f"float-{min_value}-{max_value}"
                                    else:
                                        attribute_types[attr] = f"digit_id-{length}"
                            elif (
                                re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", attr_values[i],)
                                or attr_values[i] == "nan"
                            ):
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if (
                                            not re.match(
                                                r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
                                                attr_values[j],
                                            )
                                            or attr_values[i] == "nan"
                                        ):
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                                if not is_field:
                                    attribute_types[attr] = f"date-"
                            elif re.match(r"^\d+\.\d+$", attr_values[i]) or attr_values[i] == "nan":
                                relative_float_type = False
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if (
                                            not re.match(r"^\d+\.?\d*$", attr_values[j])
                                            or attr_values[j] == "nan"
                                        ):
                                            if re.match(r"^-\d+\.?\d*$", attr_values[j]):
                                                relative_float_type = True
                                            else:
                                                attribute_types[attr] = f"field-{attr}"
                                                possible_values[f"{attr}"] = attr_values
                                                is_field = True
                                                break
                                if not is_field:
                                    if relative_float_type:
                                        min_value = min(
                                            [float(x) for x in attr_values if float(x) > 0]
                                        )
                                        max_value = max(
                                            [float(x) for x in attr_values if float(x) > 0]
                                        )
                                        attribute_types[
                                            attr
                                        ] = f"relative_float-{min_value}-{max_value}"
                                    else:
                                        min_value = min([float(x) for x in attr_values])
                                        max_value = max([float(x) for x in attr_values])
                                        attribute_types[attr] = f"float-{min_value}-{max_value}"
                            elif (
                                re.match(r"^-\d+\.?\d*$", attr_values[i]) or attr_values[i] == "nan"
                            ):
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if (
                                            not re.match(r"^-\d+\.?\d*$", attr_values[j])
                                            or attr_values[j] == "nan"
                                        ):
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[
                                                f"{filename.split('.')[0]}-{attr}"
                                            ] = attr_values
                                            is_field = True
                                            break
                                if not is_field:
                                    min_value = min(
                                        [abs(float(x)) for x in attr_values if float(x) > 0]
                                    )
                                    max_value = max([float(x) for x in attr_values if float(x) > 0])
                                    attribute_types[
                                        attr
                                    ] = f"relative_float-{min_value}-{max_value}"
                            elif re.match(r"^\d{5}-\d{5}$", attr_values[i]):
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if not re.match(r"^\d{5}-\d{5}$", attr_values[j]):
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                                if not is_field:
                                    attribute_types[attr] = f"double_digit_id-5"
                            elif re.match(r"^\d+-\d$", attr_values[i]) or attr_values[i] == "nan":
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if (
                                            not re.match(r"^\d+-\d$", attr_values[j])
                                            or attr_values[j] == "nan"
                                        ):
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                                if not is_field:
                                    attribute_types[attr] = f"composed_digit_id-"
                            elif re.match(r"^[EV]?\d+$", attr_values[i]):
                                is_field = False
                                for j in range(i + 1, len(attr_values)):
                                    if attr_values[j] != "":
                                        if not re.match(r"^[EV]?\d+$", attr_values[j]):
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                                if not is_field:
                                    attribute_types[attr] = f"ev_digit_id-"
                        else:
                            attribute_types[attr] = f"field-{attr}"
                            possible_values[f"{attr}"] = attr_values
                    except IndexError:
                        print(f"Attributed ignored : empty column {attr} in table {filename}.")

                with open(f"{self.dest_folder}/csv_unique_values/{filename}", "w+") as f:
                    writer = csv.writer(f)
                    writer.writerow(unique_values.keys())
                    max_len = max(len(unique_values[x]) for x in attr_list)
                    i = 0
                    while i < max_len:
                        row = []
                        for attr in attr_list:
                            values = unique_values[attr]
                            if i < len(values):
                                row.append(values[i])
                            else:
                                row.append("")
                        writer.writerow(row)
                        i += 1
                attribute_types_all_tables[filename.split(".")[0].lower()] = attribute_types
                possible_values_all_tables[filename.split(".")[0].lower()] = possible_values
                f_count += 1

        print("\nInferring terminated !\n")
        return attribute_types_all_tables, possible_values_all_tables

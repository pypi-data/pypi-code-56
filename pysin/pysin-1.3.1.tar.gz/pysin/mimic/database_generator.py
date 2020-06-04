from faker import Factory
from random import choice, choices, randint, random, shuffle


class DataBaseRandomGenerator:
    def __init__(self, locale="fr_FR"):
        self._fake_factory = Factory.create(locale)
        self.locale = locale
        self.tables = {}
        self._possible_values = {}
        self.relations = {}

    def add_table(self, name, table):
        assert not name in self.tables, f"The table {name} already exists."
        self.tables[name] = table
        self._possible_values[name] = {}

    def add_relation(self, name, relation_dict):
        assert (
            type(relation_dict) == dict
            and "parents" in relation_dict.keys()
            and "children" in relation_dict.keys()
        ), "A relation must be a dict following the pattern {'parents': (table, attribute), 'children': (table, attribute, type)}."
        test_table_name, test_attr_name = relation_dict["parents"][0]
        attribute_type = (
            self.tables[test_table_name].attributes[test_attr_name].attr_type.type_name
        )
        assert name not in self.relations, f"The relation {name} already exists."
        assert (
            test_table_name in self.tables.keys()
        ), f"A relation uses the table {test_table_name} whereas this table does not exist."
        for table_name, attr_name in relation_dict["parents"]:
            assert (
                table_name in self.tables.keys()
            ), f"A relation uses the table {table_name} whereas this table does not exist."
            assert (
                attr_name in self.tables[table_name].attributes.keys()
            ), f"A relation uses the attribute {attr_name} from table {table_name} whereas this attribute does not exist."
            assert (
                self.tables[table_name].attributes[attr_name].attr_type.type_name
                == attribute_type
            ), f"The following attributes are in relation but their types are different : {attr_name} from {table_name} (of type {self.tables[table_name].attributes[attr_name].attr_type.type_name}) and {test_attr_name} from {test_table_name} (of type {attribute_type})."
        for table_name, attr_name, _ in relation_dict["children"]:
            assert (
                table_name in self.tables.keys()
            ), f"A relation uses the table {table_name} whereas this table does not exist."
            assert (
                attr_name in self.tables[table_name].attributes.keys()
            ), f"A relation uses the attribute {attr_name} from table {table_name} whereas this attribute does not exist."
            assert (
                self.tables[table_name].attributes[attr_name].attr_type.type_name
                == attribute_type
            ), f"The following attributes are in relation but their types are different : {attr_name} from {table_name} (of type {self.tables[table_name].attributes[attr_name].attr_type.type_name}) and {test_attr_name} from {test_table_name} (of type {attribute_type})."
        self.relations[name] = relation_dict

    def _satisfy_relation(
        self, relation_dict, min_rows=10, max_card=5, missing_rate=0.1
    ):
        test_table_name, test_attr_name = relation_dict["parents"][0]
        length = max(
            [
                self.tables[table_name].length()
                for table_name, _ in relation_dict["parents"]
            ]
        )
        attribute_class = self.tables[test_table_name].attributes[test_attr_name]
        for table_name, attr_name in relation_dict["parents"]:
            assert self.tables[table_name].length() in {
                0,
                length,
            }, f"The tables {test_table_name} and {table_name} are in relation one-to-one with the attributes {test_attr_name} = {attr_name} but their length are different : {length} != {self.tables[table_name].length}."
        if not length:
            length = min_rows
        possible_values = []
        if attribute_class.attr_type.type_name == "field":
            possible_values = attribute_class.kwargs_rd_gen["possible_values"].to_list()
        else:
            for _ in range(length):
                val = attribute_class.get_random_value(self._fake_factory, self.locale)
                while val in possible_values:
                    val = attribute_class.get_random_value(
                        self._fake_factory, self.locale
                    )
                possible_values.append(val)
        length_possible_values = len(possible_values)
        for table_name, attr_name in relation_dict["parents"]:
            self._possible_values[table_name][attr_name] = possible_values
        for table_name, attr_name, rel_type in relation_dict["children"]:
            assert rel_type != (2, 2), "Cannot handle (2,2) relations yet."
            if rel_type == (0, 1):
                length = self.tables[table_name].length()
                if length == 0:
                    self._possible_values[table_name][attr_name] = []
                    for val in possible_values:
                        if random() > missing_rate:
                            self._possible_values[table_name][attr_name].append(val)
                else:
                    assert (
                        length <= length_possible_values
                    ), f"Not enough values to fit in attribute {attr_name} from {table_name}."
                    self._possible_values[table_name][attr_name] = choices(
                        possible_values, k=length
                    )
            elif rel_type == (0, 2):
                length = self.tables[table_name].length()
                shuffle(possible_values)
                current_possible_values = possible_values[
                    : int(length_possible_values * (1 - missing_rate))
                ]
                if length == 0:
                    self._possible_values[table_name][attr_name] = choices(
                        current_possible_values, k=int(min_rows * max_card / 2)
                    )
                else:
                    assert length >= len(
                        possible_values
                    ), f"Too many values to fit in attribute {attr_name} from table {table_name}."
                    self._possible_values[table_name][attr_name] = choices(
                        current_possible_values, k=length
                    )
            elif rel_type == (1, 2):
                length = self.tables[table_name].length()
                if length == 0:
                    current_possible_values = possible_values + choices(
                        possible_values, k=int(min_rows * max_card / 2) - 1
                    )
                    shuffle(current_possible_values)
                    self._possible_values[table_name][
                        attr_name
                    ] = current_possible_values
                else:
                    assert length >= len(
                        possible_values
                    ), f"Too many values to fit in attribute {attr_name} from table {table_name}."
                    current_possible_values = possible_values + choices(
                        possible_values, k=length - length_possible_values
                    )
                    shuffle(current_possible_values)
                    self._possible_values[table_name][
                        attr_name
                    ] = current_possible_values

    def random_generation(self, min_rows=100, max_card=5, missing_rate=0.1):

        print("Starts filling table...")
        nb_relations = len(self.relations)
        r = 0
        for _, relation_dict in self.relations.items():
            print(
                f"Satisfying relations : {int(50 * (r + 1) / nb_relations) * '■' + int(50 * (1 - (r + 1) / nb_relations)) * '_'}",
                end="\r",
            )
            self._satisfy_relation(
                relation_dict,
                min_rows=min_rows,
                max_card=max_card,
                missing_rate=missing_rate,
            )
            r += 1
        print("\n")
        nb_tables = len(self.tables)
        t = 0
        for table in self.tables:
            print(
                f"Filling columns      : {int(50 * (t + 1) / nb_tables) * '■' + int(50 * (1 - (t + 1) / nb_tables)) * '_'}",
                end="\r",
            )
            for i in range(
                min(
                    [min_rows]
                    + [
                        len(self._possible_values[table][attr])
                        for attr in self._possible_values[table].keys()
                    ]
                )
            ):
                self.tables[table].add_random_row(
                    self._fake_factory,
                    self.locale,
                    fixed_values={
                        attr: values[i]
                        for attr, values in self._possible_values[table].items()
                    },
                )
            t += 1
        print("\nDatabase filled !")

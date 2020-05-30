"""Class to describe features of the Heritage Health dataset."""
from ethicml.data import Dataset

__all__ = ["health"]


def health(split: str = "Sex", discrete_only: bool = False) -> Dataset:
    """Heritage Health dataset."""
    if True:  # pylint: disable=using-constant-test
        features = [
            "MemberID_t",
            "YEAR_t",
            "ClaimsTruncated",
            "trainset",
            "age_05",
            "age_15",
            "age_25",
            "age_35",
            "age_45",
            "age_55",
            "age_65",
            "age_75",
            "age_85",
            "age_MISS",
            "sexMALE",
            "sexFEMALE",
            "sexMISS",
            "no_Claims",
            "no_Providers",
            "no_Vendors",
            "no_PCPs",
            "no_PlaceSvcs",
            "no_Specialities",
            "no_PrimaryConditionGroups",
            "no_ProcedureGroups",
            "PayDelay_max",
            "PayDelay_min",
            "PayDelay_ave",
            "PayDelay_stdev",
            "LOS_max",
            "LOS_min",
            "LOS_ave",
            "LOS_stdev",
            "LOS_TOT_UNKNOWN",
            "LOS_TOT_SUPRESSED",
            "LOS_TOT_KNOWN",
            "dsfs_max",
            "dsfs_min",
            "dsfs_range",
            "dsfs_ave",
            "dsfs_stdev",
            "CharlsonIndexI_max",
            "CharlsonIndexI_min",
            "CharlsonIndexI_ave",
            "CharlsonIndexI_range",
            "CharlsonIndexI_stdev",
            "pcg1",
            "pcg2",
            "pcg3",
            "pcg4",
            "pcg5",
            "pcg6",
            "pcg7",
            "pcg8",
            "pcg9",
            "pcg10",
            "pcg11",
            "pcg12",
            "pcg13",
            "pcg14",
            "pcg15",
            "pcg16",
            "pcg17",
            "pcg18",
            "pcg19",
            "pcg20",
            "pcg21",
            "pcg22",
            "pcg23",
            "pcg24",
            "pcg25",
            "pcg26",
            "pcg27",
            "pcg28",
            "pcg29",
            "pcg30",
            "pcg31",
            "pcg32",
            "pcg33",
            "pcg34",
            "pcg35",
            "pcg36",
            "pcg37",
            "pcg38",
            "pcg39",
            "pcg40",
            "pcg41",
            "pcg42",
            "pcg43",
            "pcg44",
            "pcg45",
            "pcg46",
            "sp1",
            "sp2",
            "sp3",
            "sp4",
            "sp5",
            "sp6",
            "sp7",
            "sp8",
            "sp9",
            "sp10",
            "sp11",
            "sp12",
            "sp13",
            "pg1",
            "pg2",
            "pg3",
            "pg4",
            "pg5",
            "pg6",
            "pg7",
            "pg8",
            "pg9",
            "pg10",
            "pg11",
            "pg12",
            "pg13",
            "pg14",
            "pg15",
            "pg16",
            "pg17",
            "pg18",
            "ps1",
            "ps2",
            "ps3",
            "ps4",
            "ps5",
            "ps6",
            "ps7",
            "ps8",
            "ps9",
            "drugCount_max",
            "drugCount_min",
            "drugCount_ave",
            "drugcount_months",
            "labCount_max",
            "labCount_min",
            "labCount_ave",
            "labcount_months",
            "labNull",
            "drugNull",
        ]

        features_to_remove = ["MemberID_t", "YEAR_t", "trainset", "sexMISS", "age_MISS"]
        features = [feature for feature in features if feature not in features_to_remove]

        continuous_features = [
            "no_Claims",
            "no_Providers",
            "no_Vendors",
            "no_PCPs",
            "no_PlaceSvcs",
            "no_Specialities",
            "no_PrimaryConditionGroups",
            "no_ProcedureGroups",
            "PayDelay_max",
            "PayDelay_min",
            "PayDelay_ave",
            "PayDelay_stdev",
            "LOS_max",
            "LOS_min",
            "LOS_ave",
            "LOS_stdev",
            "LOS_TOT_UNKNOWN",
            "LOS_TOT_SUPRESSED",
            "LOS_TOT_KNOWN",
            "dsfs_max",
            "dsfs_min",
            "dsfs_range",
            "dsfs_ave",
            "dsfs_stdev",
            "CharlsonIndexI_max",
            "CharlsonIndexI_min",
            "CharlsonIndexI_ave",
            "CharlsonIndexI_range",
            "CharlsonIndexI_stdev",
            "pcg1",
            "pcg2",
            "pcg3",
            "pcg4",
            "pcg5",
            "pcg6",
            "pcg7",
            "pcg8",
            "pcg9",
            "pcg10",
            "pcg11",
            "pcg12",
            "pcg13",
            "pcg14",
            "pcg15",
            "pcg16",
            "pcg17",
            "pcg18",
            "pcg19",
            "pcg20",
            "pcg21",
            "pcg22",
            "pcg23",
            "pcg24",
            "pcg25",
            "pcg26",
            "pcg27",
            "pcg28",
            "pcg29",
            "pcg30",
            "pcg31",
            "pcg32",
            "pcg33",
            "pcg34",
            "pcg35",
            "pcg36",
            "pcg37",
            "pcg38",
            "pcg39",
            "pcg40",
            "pcg41",
            "pcg42",
            "pcg43",
            "pcg44",
            "pcg45",
            "pcg46",
            "sp1",
            "sp2",
            "sp3",
            "sp4",
            "sp5",
            "sp6",
            "sp7",
            "sp8",
            "sp9",
            "sp10",
            "sp11",
            "sp12",
            "sp13",
            "pg1",
            "pg2",
            "pg3",
            "pg4",
            "pg5",
            "pg6",
            "pg7",
            "pg8",
            "pg9",
            "pg10",
            "pg11",
            "pg12",
            "pg13",
            "pg14",
            "pg15",
            "pg16",
            "pg17",
            "pg18",
            "ps1",
            "ps2",
            "ps3",
            "ps4",
            "ps5",
            "ps6",
            "ps7",
            "ps8",
            "ps9",
            "drugCount_max",
            "drugCount_min",
            "drugCount_ave",
            "drugcount_months",
            "labCount_max",
            "labCount_min",
            "labCount_ave",
            "labcount_months",
        ]

        if split == "Sex":
            sens_attrs = ["sexMALE"]
            s_prefix = ["sex"]
            class_labels = ["Charlson>0"]
            class_label_prefix = ["Charlson"]
        else:
            raise NotImplementedError
    return Dataset(
        name="Health",
        num_samples=171067,
        filename_or_path="health.csv.zip",
        features=features,
        cont_features=continuous_features,
        s_prefix=s_prefix,
        sens_attrs=sens_attrs,
        class_label_prefix=class_label_prefix,
        class_labels=class_labels,
        discrete_only=discrete_only,
    )

import pandas as pd


def denuder(compiled, acquisition, results):
    import numpy as np

    np.seterr(divide="ignore", invalid="ignore")
    compiled = compiled.set_index("Topic ID")
    acquisition = pd.concat(acquisition, sort=False).set_index("Topic ID").sort_index()
    re = pd.concat(results, sort=False).set_index("Topic ID").sort_index()
    acquisition["Denuder type"] = acquisition["Denuder type"].apply(lambda x: x.lower())
    data_groups = acquisition.groupby("Ratio W/Wo - Topic comparison")
    cframes = []
    for id, frames in data_groups:
        if data_groups.groups.get(id).size == 2:
            index = frames.index
            denuder = re.loc[index][
                ~acquisition.loc[index]["Denuder type"].isin(["no"])
            ]
            not_denuder = re.loc[index][
                acquisition.loc[index]["Denuder type"].isin(["no"])
            ]
            calculated_frame = pd.DataFrame(
                columns=re.columns, data=denuder.values / not_denuder.values
            ).add_suffix(" Ratio Denuder/No Denuder")
            topics = "-".join(
                list(map(lambda x: str(x), [denuder.index[0], not_denuder.index[0]]))
            )
            calculated_frame["Ratio for Denuder Topic IDs"] = topics
            cframes.append(calculated_frame)
    cc = pd.concat(cframes)
    cc = cc.reset_index()
    cc = cc.drop(columns=["index"])
    for ind, frame in cc.iterrows():
        working_frame = pd.DataFrame(cc.iloc[ind]).transpose()
        topic_list = frame["Ratio for Denuder Topic IDs"].split("-")
        for id in topic_list:
            id = int(id)
            for key, value in working_frame.iteritems():
                compiled.loc[id, key] = value.values[0]
    compiled.reset_index(inplace=True)
    return compiled


def cross_topic(compiled, acquisition, results):

    results = pd.concat(results, sort=False).set_index("Topic ID").sort_index()
    acquisition = pd.concat(acquisition, sort=False).set_index("Topic ID").sort_index()
    acquisition = acquisition.applymap(
        lambda x: x.casefold() if isinstance(x, str) else x
    )
    acquisition_duplicates = acquisition[
        acquisition.drop(columns="Ratio W/Wo - Topic comparison").duplicated()
    ]
    compiled = compiled.set_index("Topic ID")
    compiled_acq_duplicates = compiled.loc[acquisition_duplicates.index]
    compiled_acq_form_duplicates = (
        compiled_acq_duplicates.groupby("formulation id")
        .filter(lambda x: x.shape[0] > 2)
        .groupby("formulation id")
    )

    stats = compiled_acq_form_duplicates[results.columns].aggregate(
        ["min", "mean", "max", "std", "count"]
    )
    rename_dictionary = {b: b.split(" ")[0] for b in stats.columns.levels[0]}
    stats = stats.rename(columns=rename_dictionary, level=0)
    thought = stats.stack().reset_index().rename(columns={"level_1": "stat"})
    # thought["formulation id"] = thought["formulation id"].str.cat(
    #    thought["stat"], sep=" "
    # )
    return thought

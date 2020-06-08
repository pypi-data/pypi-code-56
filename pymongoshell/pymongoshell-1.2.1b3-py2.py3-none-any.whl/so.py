to_be_inserted = []
for d in candidate_records:

    if col.find_one(d["_id"]):
        continue
    else:
        to_be_inserted.append(d)

if len(d) > 0:
    col.insert_many(to_be_inserted)

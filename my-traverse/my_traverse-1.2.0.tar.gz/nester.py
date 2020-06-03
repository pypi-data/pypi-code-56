# movies = ["The Holy Grail", "The Life of Brian", "The Meaning of Life"]
# movies.insert(1,1975);
# movies.insert(3, 1979);
# movies.insert(5, 1983);
# # print(movies);
#
# movies = ['The Holy Grail', 1975, 'Terry Jones & Terry Gilliam', 91, ['Graham Chapman', ['Michael Palin',
# 'John Cleese', 'Terry Gilliam', 'Eric Idle', 'Terry Jones']]]
#
# cute_mom = [
#     "Mengfei Yang",
#     30.75,
#     True,
#     ["Pink", "Coffee","Lovely"]
# ]

def traverse_list(list_par, apply_indent=False,level=-1):
    if isinstance(list_par, list):
        for list_item in list_par:
            traverse_list(list_item,apply_indent, level+1)
    else:
        indent="";
        if apply_indent:
            for time in range(level):
                # indent += "\t"
                print(end="\t")
        print(indent+str(list_par))
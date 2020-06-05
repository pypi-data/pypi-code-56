
class Athles:
    def __init__(self, a_name, a_dob=None, a_times=[]):
        self.a_name = a_name
        self.a_dob = a_dob
        self.a_times=a_times


    def how_big(self):
        return ()

    # def sanitize(self):

    def top3(self):
        sanitized_timmings = [sanitize(each_timing) for each_timing in self.a_times]
        unique_james = sorted(set(sanitized_timmings))
        return (unique_james[0:3])

    def add_time(self, new_time):
        self.a_times.append(new_time)
    def add_times(self, new_times):
        self.a_times.extend(new_times)

def sanitize(time_string):
     if "-" in time_string:
        spliter = "-"
     elif ":" in time_string:
        spliter = ":"
     else:
        return (time_string)
     (min, sec) = time_string.split(spliter)
     return (min + "." + sec)


sarah = Athles('Sarah Sweeney', '2002-6-7', ['2:58', '2.58', '1.56'])
james = Athles('James')
print(type(james))
print(james.__class__)
print(james.a_name)
print(sarah.top3())




cleese={}
palin=dict()
cleese["Name"] = "John Cleese"
cleese["Occupations"] = ['actor', 'comedian', 'writer', 'film producer']
palin={"Name":"Michael Palin", "Occupations":['comedian', 'actor', 'writer', 'tv']}
print(cleese)
print(palin["Occupations"][-1])

data = [6,3,1,2,4,5]
print([each_item*60 for each_item in data])
# print(sorted(data))
# print(data);
# print(data.sort());
# print(data);



formated_time = sanitize("2-25")
print(formated_time)

try:
    with open("james.txt") as jaf, open("julie.txt") as juf, open("mikey.txt") as mif, open("sarah.txt") as saf:
        ja_data = jaf.readline()
        james = ja_data.strip().split(",")
        c_james=[sanitize(each_line) for each_line in james]
        ju_data = juf.readline()
        julie = ju_data.strip().split(",")
        c_julie=[sanitize(each_line) for each_line in julie]
        mi_data = mif.readline()
        mikey = mi_data.strip().split(",")
        c_mikey= [sanitize(each_line) for each_line in mikey]
        sa_data = saf.readline()
        sarar = sa_data.strip().split(",")
        c_sarar = [sanitize(each_line) for each_line in sarar]
        print("------------------------Original Time--------------------------")
        print(james)
        print(julie)
        print(mikey)
        print(sarar)
        print("------------------------Directly Sorted--------------------------")
        print(sorted(james))
        print(sorted(julie))
        print(sorted(mikey))
        print(sorted(sarar))
        print("------------------------Converted Sorted--------------------------")
        print(sorted(c_james))
        print(sorted(c_julie))
        print(sorted(c_mikey))
        print(sorted(c_sarar))
except IOError as ioerr:
    print("IO Error: " + str(ioerr))

unique_james=[]
for item in c_james:
    if item not in unique_james:
        unique_james.append(item)
print(sorted(unique_james))
unique_james = set(c_james)
print(sorted(unique_james));


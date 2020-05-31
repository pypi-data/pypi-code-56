import mozen_zoo.models as m

print('DEBUT DU PROGRAMME APPELANT \n')
r = m.load("7","r")
with r as f:
    print("Keys: \n %s" % f.keys())
    #Get the keys
    a_group_key = list(f.keys())[0]
    # Get data
    data = list(f[a_group_key])
    print("\n DATA : \n \n %s" % data)

    print("\n \n FIN DU PROGRAMME !!!")




    
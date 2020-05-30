from . import services, status

def get_all_notes_representation():
    print(services.get_status(1))
    print(status.Status['CREATED'])
    notes = services.get_notes()
    n = [format(list(x)) for x in notes]
    print(n)
    return 'test'

def format(x):
    # Add status text representation
    x[4] = services.get_status(x[4]).value[2]
    return x

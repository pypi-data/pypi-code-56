with open("config.py", "r") as f:
    config = f.read()
print(config.find("appToken"))
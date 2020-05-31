import aimslib.detailed_roster.process as dr

s = open("/home/jon/docs/easyjet/roster/roster-202002.htm").read()
print(dr.crew(s))

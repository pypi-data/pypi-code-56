from .extractor import *
import pkg_resources


resource_package = 'VTEReportsAnalysis'
resource_path = '/'.join(('config','config.txt'))
path = pkg_resources.resource_filename(resource_package, resource_path)

target = []
skip = []
absolute_negative = []
absolute_positive = []
start = []

active_section = 0

with open(path, 'r') as config:
	lines = config.readlines()
	lines.remove('\n')
	for line in lines:
		if line == '':
			continue
		if '#target_phrases' in line:
			active_section = target
		elif '#skip_phrases' in line:
			active_section = skip
		elif '#absolute_negative' in line:
			active_section = absolute_negative
		elif '#absolute_positive' in line:
			active_section = absolute_negative
		elif 'start' in line:
			active_section = start
		if '#' not in line:
			active_section.append(line.strip())

config.close()
#print(target)

phrases =[target,skip,absolute_negative,absolute_positive,start]
for phrase in phrases:
	while '' in phrase:
		phrase.remove('')

extractors = reExtractor(target, skip, absolute_negative, absolute_positive, start)

def extraction(text):
	return extractors.processing(text)


'''
print(extractor.processing('in the body'))
'''
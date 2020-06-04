import csv, zipfile, os
import requests
from datetime import datetime, timedelta
from io import TextIOWrapper, StringIO

months = {
    '01': {'name':'JAN', 'days': 31},
    '02': {'name':'FEB', 'days': 29},
    '03': {'name':'MAR', 'days': 31},
    '04': {'name':'APR', 'days': 30},
    '05': {'name':'MAY', 'days': 31},
    '06': {'name':'JUN', 'days': 30},
    '07': {'name':'JUL', 'days': 31},
    '08': {'name':'AUG', 'days': 31},
    '09': {'name':'SEP', 'days': 30},
    '10': {'name':'OCT', 'days': 31},
    '11': {'name':'NOV', 'days': 30},
    '12': {'name':'DEC', 'days': 31},
}

def fetch(url_template, date, target_dir, zipped, columns):
    url = url_from_template(url_template, date)
    if (zipped):
        target_zip = target_dir+'/'+ date+'.zip'
        if not os.path.exists(target_dir+'/csv'):
            os.mkdir(target_dir+'/csv')
        target_csv = target_dir+'/csv/'+ date+'.csv'
    else:
        if not os.path.exists(target_dir+'/csv'):
            os.mkdir(target_dir+'/csv')
        target_zip = target_dir+'/csv'+ date+'.csv'
        target_csv = target_zip

    print("fetching from %s into %s " % (url, target_zip))
        # get request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        # write to file
        with open(target_zip, "wb") as file:
            file.write(response.content)
            if zipped:
                data = unzip(target_zip)
                if columns.find('DATE') == -1:
                    writeCSV(data, target_csv, columns, addDate=True, date=date)
                else:
                    writeCSV(data, target_csv, columns)
    except requests.exceptions.HTTPError as errh:
        # print (errh.response.text)
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)


def unzip(source):
    print("unzipping %s" % (source))
    with zipfile.ZipFile(source, "r") as zip_ref:
        for file in zip_ref.namelist():
            print("Extracting %s from zip" % file)
            data = []
            with zip_ref.open(file) as myfile:
                reader = csv.reader(TextIOWrapper(myfile, 'utf-8'))
                for row in reader:
                    data.append(row)
            return data
                        
                

def writeCSV(data, target, header, addDate=False, date=None):
    linecount = 0
    if addDate:
        header = 'DATE,'+ header
    f = StringIO(header)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        print('Setting headers',row)
        header_row =row
    with open(target, "w") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for row in data:
            # print(row)
            if linecount == 0:
                 print('Incoming headers',row)
                 csv_writer.writerow(header_row)
                 linecount+=1
            else:
                if addDate:
                    row.insert(0, date[4:6]+'/'+ date[6:] + '/'+date[:4])
                csv_writer.writerow(row)
                linecount+=1


def readCSV(source):
    data = []
    line_count = 0
    with open(source, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line_count += 1
                data.append(row)
    return data

def today():
    return datetime.today().strftime('%Y%m%d')

def url_from_template(template, date):
    template = template.replace('#-#day#-#', date[6:])
    template = template.replace('#-#month#-#', date[4:6])
    template = template.replace('#n#month#n#', months[date[4:6]]['name'])
    template = template.replace('#-#year#-#', date[:4])
    template = template.replace('#-#YY#-#', date[2:4])
    return template

def dateList(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    dates = [x.strftime('%Y%m%d') for x in date_generated]

    return dates

import libABCD
import json

# Can be multiple messages, so raw_decode in that case, and call relevant function(s)
def parsemsg(data,connection):
    try:
        dec = json.JSONDecoder()
        pos = 0
        json_str=str(data.decode())
        while not pos == len(json_str):
            jsdata, json_len = dec.raw_decode(json_str[pos:])
            pos += json_len
            try:
                if jsdata["cmd"] in libABCD.cmd_switch:
                    func=libABCD.cmd_switch[jsdata["cmd"]]
                else:
                    func=libABCD.cmd_switch["_default"]
            except Exception as e:
                libABCD.logger.warning('Don\'t know what to do with message {} from {}'.format(jsdata,connection.getpeername()))
            else:
                try:
                    func(jsdata,connection)
                except Exception as e:
                    libABCD.logger.error('Function call error {} for message {} from {}'.format(e,jsdata,connection.getpeername()))
    except Exception as e:
        libABCD.logger.error('Couldn\'t parse message {} from {}',format(data,connection.getpeername()))


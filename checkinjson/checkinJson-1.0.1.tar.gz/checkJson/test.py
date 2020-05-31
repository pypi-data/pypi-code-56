from checkjson import check
import json
from pprint import pprint


sub = {"code": 200,
       "error": "hello, world",
       "name": "<name>",
       "phone": "<phone>",
       "level": [1],
       "address": "china",
       "result": [
           {"sweetest": "OK",
            "status": "<status>"
            },
           {"ages": [1, 2, 4],
            "status": "yes"
            },
           {"sonar": "OK",
            "status": "yes",
            "fruit": ["apple"]
            }
       ],
       "student":{"name": "daben",
            "age": "<age>"
           }
       }

parent = {"code": 200,
          "error": "you are bad",
          "name": "daben1",
          "level": [2,1,"ONE"],
          "address": 86,
          "result": [
              {"test01": "Fail",
               "status": "NO"
               },
              {"test01": "OK",
               "status": "NO"
               },
              {"ages": [1, 2, 3],
               "status": "yes"
               },
              {"sonar": "OK",
               "status": "yes",
               "fruit": ["branana",'orange']
               }
          ],
          "student":{"name": "daben123",
               "age": 19
              }
          }

result = check(sub, parent)
# pprint(json.dumps(result, ensure_ascii=False, indent=4))
pprint(result)
'''
WikiMedia API command line interface.

An attempt to make it easier to use the API.

James Gardner

'''


import json
import requests as rq



def main():
    url = "https://en.wikipedia.org/w/api.php?"
    headers = {
        "User-Agent": "CarletonComps2020/0.1 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
        "Connection": "close"
    }


    valid = False
    while (not valid):
        print("Enter page to export to HTML. Separate words with underscore (_). Single page only.: ")
        page = input()
        numargs = len(page.split())
        if (numargs != 1):
            valid = False
            print("Single page only. Enter page to export to HTML. Separate words with underscore (_).")
            page=input()
        else:
            valid = True

    valid = False
    while (not valid):
        print("Enter revision ID (oldid) of page. Numbers only.")
        id = input()
        numargs = len(id.split())
        try:
            id = int(id)
            isNum = True
        except:
            isNum = False
        if (numargs != 1 and isNum == False):
            valid = False
            print("Invalid input. Please enter revision ID (oldid) of page. Numbers only.")
            id = input()
            try:
                id = int(id)
                isNum = True
            except:
                isNum = False
        else:
            valid = True


    params = {
        "action": "parse",
        # "text": page,
        "oldid": id,
        "format": "json"
    }
    data = rq.get(url=url, headers=headers, params=params).json()
    # for key in data['error'].keys():
    #     print(data['error'][key])
    f = data['parse']['text']['*']

    filename = page + ".html"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f)
    
    print("Output file {0} was created.".format(filename))

if (__name__=="__main__"):
    main()
a = 1
b = 11
c = 111
d = 1111

version = 1
quality = ["DOMESTIC","EXPORT","COMMON"]

compny_name = "KI"

data = [{"id":1,"name":"PART1","version":1,"quality":"COMMON"},
        {"id":11,"name":"PART1","version":1,"quality":"COMMON"},
        {"id":111,"name":"PART1","version":1,"quality":"COMMON"},
        {"id":1111,"name":"PART1","version":1,"quality":"COMMON"}
        ]

for i in data:
    part_code = None
    if len(str(i['id'])) == 1:
        id = "000" + str(i['id'])
    elif len(str(i['id'])) == 2:
        id = "00" + str(i['id'])
    elif len(str(i['id'])) == 3:
        id = "0" + str(i['id'])
    else:
        id = str(i['id'])

    part_code = compny_name + str(i['version']) + str(i['quality'][:1]) + id
    print(part_code)

    



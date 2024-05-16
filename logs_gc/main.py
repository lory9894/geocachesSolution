import xml.etree.ElementTree as ET
import json


def parse_gpx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def get_caches(root):
    children = root.findall('{http://www.topografix.com/GPX/1/0}wpt')

    caches = []
    for child in children:
        cache = child.findall('{http://www.groundspeak.com/cache/1/0}cache')
        cache[0].attrib['gc_code'] = child.findall('{http://www.topografix.com/GPX/1/0}name')[0].text
        caches.append(cache[0])

    return caches

def jsonify(dict,filename="out.json"):
    jsonstring = json.dumps(dict, indent=4, ensure_ascii=False)
    with open(filename, "w") as f:
        f.write(jsonstring)
    return jsonstring

def main():
    root = parse_gpx("logs.gpx")
    #get waypoints
    caches = get_caches(root)

    log_dict = {}
    caches.sort(key=lambda x: x.find('{http://www.groundspeak.com/cache/1/0}logs').find('{http://www.groundspeak.com/cache/1/0}log').find('{http://www.groundspeak.com/cache/1/0}date').text)
    for cache in caches:
        my_log = cache.find('{http://www.groundspeak.com/cache/1/0}logs').find('{http://www.groundspeak.com/cache/1/0}log').find('{http://www.groundspeak.com/cache/1/0}text').text
        date = cache.find('{http://www.groundspeak.com/cache/1/0}logs').find('{http://www.groundspeak.com/cache/1/0}log').find('{http://www.groundspeak.com/cache/1/0}date').text
        link = f"https://coord.info/{cache.attrib['gc_code']}"
        log_dict[cache.find('{http://www.groundspeak.com/cache/1/0}name').text] = (date, my_log,link )

    print(jsonify(log_dict))

if __name__ == "__main__":
    main()
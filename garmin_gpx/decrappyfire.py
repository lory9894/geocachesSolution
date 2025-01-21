from lxml import etree as ET
tree= ET.parse("habt.gpx")
root = tree.getroot()

for child in root.findall("{http://www.topografix.com/GPX/1/0}wpt"):
    if child.find("{http://www.topografix.com/GPX/1/0}type").text.find("Waypoint") != -1:
        root.remove(child)
    else:
        child.find("{http://www.topografix.com/GPX/1/0}type").text = "Geocache" #TODO: testare perchè non so il garmin come la prende.
        filler = child.find("{http://www.groundspeak.com/cache/1/0/1}cache")
        child.remove(filler)
        filler = child.find("{http://www.gsak.net/xmlv1/6}wptExtension")
        child.remove(filler)
        filler = child.find("{http://www.cgeo.org/wptext/1/0}cacheExtension")
        child.remove(filler)

tree.write("habt2.gpx", xml_declaration=False, encoding='utf-8')



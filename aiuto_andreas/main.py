from geopy import distance
import re
import csv
import gpxpy.gpx


def ddm2dec(dms_str):

    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute_decimal = numbers[1]
    decimal_val = numbers[2] if len(numbers) > 2 else '0'
    minute_decimal += "." + decimal_val

    return sign * (int(degree) + float(minute_decimal) / 60)


max_distance = 3.22
original = (ddm2dec("N 45° 50.000'"), ddm2dec("E 009° 32.500'"))
val_list = [632,634,636,638,640,642,644,646,648,650,652,877,879,881,883,885,887,889,891,893,895]

possible_coordinates = []
readable_coordinates = []
for i in range(0, len(val_list)):
    for j in range(0, len(val_list)):
        coord = (ddm2dec(f"N 45° 49.{val_list[i]}'"), ddm2dec(f"E 009° 32.{val_list[j]}'"))
        if distance.distance(original, coord).km < max_distance:
            possible_coordinates.append(coord)
            readable_coordinates.append(f"N 45° 49.{val_list[i]}' E 009° 32.{val_list[j]}'")



with open('coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(possible_coordinates)

with open('readable_coords.txt', 'w', newline='') as file:
    for coord in readable_coordinates:
        file.write(str(coord) + "\n")

gpx = gpxpy.gpx.GPX()
for i in range(0, len(possible_coordinates)):
    coord = possible_coordinates[i]
    gpx_waypoint = gpxpy.gpx.GPXWaypoint(latitude=coord[0], longitude=coord[1])
    gpx_waypoint.comment = readable_coordinates[i]
    gpx.waypoints.append(gpx_waypoint)

with open("output.gpx", "w", ) as file:
    file.write(gpx.to_xml())
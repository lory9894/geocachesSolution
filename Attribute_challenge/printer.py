import random
import os
import requests
from PIL import Image, ImageDraw, ImageFont


attributes_icons = {
"Wheelchair accessible" : "wheelchair",
"Recommended for kids" : "kids",
"Stroller accessible" : "stroller",
"Dogs" : "dogs",
"Scenic view" : "scenic",
"Available 24/7" : "available",
"Takes less than one hour" : "onehour",
"Park and grab" : "parkngrab",
"Parking nearby" : "parking",
"Access/parking fee" : "fee",
"Yard (private residence)" : "frontyard",
"Bicycles" : "bicycles",
"Short hike (<1 km)" : "hike_short",
"Medium hike (1 km–10 km)" : "hike_med",
"Long hike (>10 km)" : "hike_long",
"Significant hike" : "hiking",
"Teamwork cache" : "teamwork",
"Night cache" : "nightcache",
"Recommended at night" : "night",
"Flashlight required" : "flashlight",
"UV light required" : "UV",
"Stealth required" : "stealth",
"Special tool required" : "s-tool",
"Recommended for tourists" : "touristOK",
"Picnic tables nearby" : "picnic",
"Public restrooms nearby" : "restrooms",
"Food nearby" : "food",
"Drinking water nearby" : "water",
"Public transportation nearby" : "public",
"Motorcycles" : "motorcycles",
"Quads" : "quads",
"Off-road vehicles" : "jeeps",
"Trucks/RVs" : "rv",
"Fuel nearby" : "fuel",
"Horses" : "horses",
"Camping nearby" : "camping",
"Campfires" : "campfires",
"Telephone nearby" : "phone",
"Seasonal access" : "seasonal",
"Available in winter" : "winter",
"Snowmobiles" : "snowmobiles",
"May require snowshoes" : "snowshoes",
"May require cross country skis" : "skiis",
"May require wading" : "wading",
"May require swimming" : "swimming",
"Boat required" : "boat",
"Scuba gear required" : "scuba",
"Tree climbing required" : "treeclimbing",
"Climbing gear required" : "rappelling",
"Difficult climb" : "climbing",
"Dangerous area" : "danger",
"Cliffs/falling rocks" : "cliff",
"Abandoned mine" : "mine",
"Abandoned structure" : "AbandonedBuilding",
"Dangerous animals" : "dangerousanimals",
"Livestock nearby" : "cow",
"Ticks" : "ticks",
"Poisonous plants" : "poisonoak",
"Thorns" : "thorn",
"Hunting area" : "hunting"
 }

def print_matrix(matrix):
    for row in matrix:
        print(row)

def translate_matrix(matrix):
    translated_matrix = [[None for column in range(len(matrix))] for row in range(len(matrix))]
    for row in range(len(matrix)):
        for column in range(len(matrix)):
            translated_matrix[row][column] =  attributes_icons[matrix[row][column]]
    return translated_matrix

def download_images():
    base_url = "https://www.geocaching.com/images/attributes/{}-yes.gif"
    output_dir = "downloaded_images"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for key, value in attributes_icons.items():
        image_url = base_url.format(value)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(output_dir, f"{value}.gif"), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {value}.gif")
        else:
            print(f"Failed to download {value}.gif")

    print("Download complete.")

def print_on_frame(attribute_matrix):
    # Load the background image
    background = Image.open(os.path.join('downloaded_images', 'frame.png'))
    size = background.size[0]


    #define the cell size
    cell_size = (size -120) // len(attribute_matrix[0])

    # Iterate over the matrix and paste the attribute images
    for row in range(len(attribute_matrix)):
        for col in range(len(attribute_matrix[row])):
            attribute = attribute_matrix[row][col]
            if attribute:
                attribute_image_path = os.path.join('downloaded_images', f"{attribute}.gif")
                if os.path.exists(attribute_image_path):
                    attribute_image = Image.open(attribute_image_path).convert("RGBA")
                    # Resize the attribute image to fit within the cell
                    attribute_image = attribute_image.resize((cell_size - 3, cell_size- 3 ), Image.Resampling.LANCZOS)
                    # Calculate the position to paste the attribute image
                    position = (58 + col * cell_size, 58 + row * cell_size)
                    background.paste(attribute_image, position, attribute_image)

    # Save the result
    background.save('output.png')

def translate_to_image_and_print_on_frame(matrix):
    if not os.path.exists('downloaded_images'):
        download_images()
    translated_matrix = translate_matrix(matrix)
    print_on_frame(translated_matrix)
    print("Done")

if __name__ == '__main__':
    matrix_size = 10
    attributes_keys = list(attributes_icons.keys())
    possibilities_matrix = [[random.choice(attributes_keys) for column in range(matrix_size)] for row in range(matrix_size)]
    translate_to_image_and_print_on_frame(possibilities_matrix)
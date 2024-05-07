import requests
import os
from PIL import Image
from io import BytesIO

def download_images_for_fish(fish_name, output_directory, num_images=10, target_size=(250, 250)):
    response = requests.get(f"https://api.inaturalist.org/v1/taxa?q={fish_name}&rank=species")
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        fish_taxon_id = data['results'][0]['id'] 
        print(f"Found taxon ID for {fish_name}: {fish_taxon_id}")

        response = requests.get(f"https://api.inaturalist.org/v1/observations?taxon_id={fish_taxon_id}&quality_grade=research&per_page={num_images}")
        data = response.json()

        if 'results' in data:
            for observation in data['results']:
                for photo in observation['photos']:
                    image_url = photo['url']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        resized_image = image.resize(target_size)
                        image_filename = os.path.join(output_directory, f"{observation['id']}.jpg")
                        resized_image.save(image_filename)
                        print(f"Downloaded and resized image: {image_filename}")
        else:
            print("No observations found for the specified fish species.")
    else:
        print("Fish species not found.")

# Example usage:
fish_name = "Largemouth Bass"  
output_directory = "eel"
download_images_for_fish(fish_name, output_directory, num_images=10, target_size=(250, 250))

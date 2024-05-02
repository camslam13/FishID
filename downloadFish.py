import requests
import os

def download_images_for_fish(fish_name, output_directory, num_images=10):
    # Search for fish species by name
    response = requests.get(f"https://api.inaturalist.org/v1/taxa?q={fish_name}&rank=species")
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        fish_taxon_id = data['results'][0]['id'] 
        print(f"Found taxon ID for {fish_name}: {fish_taxon_id}")

        # Search for observations of the fish species
        response = requests.get(f"https://api.inaturalist.org/v1/observations?taxon_id={fish_taxon_id}&quality_grade=research&per_page={num_images}")
        data = response.json()

        if 'results' in data:
            for observation in data['results']:
                # Get image URLs from observation
                for photo in observation['photos']:
                    image_url = photo['url']
                    # Download image
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_filename = os.path.join(output_directory, f"{observation['id']}.jpg")
                        with open(image_filename, 'wb') as image_file:
                            image_file.write(image_response.content)
                        print(f"Downloaded image: {image_filename}")
        else:
            print("No observations found for the specified fish species.")
    else:
        print("Fish species not found.")

# Example usage:
fish_name = "catfish"  
output_directory = "catfish"
download_images_for_fish(fish_name, output_directory, num_images=100)

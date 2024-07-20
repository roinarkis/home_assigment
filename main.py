from collections import defaultdict

from dtos.animal import Animal
from scraper import Scraper
from soup_fetcher import SoupFetcher
from constants import BASE_URL
from pictures_handler import PictureHandler


def create_adjective_to_animals_for_display() -> dict[str:Animal]:
    soup_fetcher = SoupFetcher(BASE_URL)
    scraper = Scraper(soup_fetcher)
    animals = scraper.get_animal_table_values()
    PictureHandler.download_images_concurrently([animal.name_for_url for animal in animals])
    adjective_to_animals = defaultdict(list)
    for animal in animals:
        for adjective in animal.collateral_adjectives:
            adjective_to_animals[adjective].append(animal)
    return adjective_to_animals


# Generate HTML content
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Animal Collateral Adjectives</title>
    <!-- Bootstrap CSS link -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
          integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
          crossorigin="anonymous">
    <style>
        .animal-table img {
            width: 80px; /* Adjust width as needed */
            height: auto;
        }
        .animal-table td {
            vertical-align: middle;
        }
        .animal-table th, .animal-table td {
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <h1 class="mt-4 mb-4">Collateral Adjectives and Animals</h1>
'''

adjective_to_animals = create_adjective_to_animals_for_display()
for adjective, animals_list in adjective_to_animals.items():
    html_content += f'''
    <h2 class="mt-4 mb-4">{adjective.capitalize()}</h2>
    <table class="table table-bordered animal-table">
        <thead class="thead-dark">
        <tr>
            <th>Name</th>
            <th>Image</th>
        </tr>
        </thead>
        <tbody>
    '''
    for animal in animals_list:
        html_content += f'''
        <tr>
            <td>{animal.name}</td>
            <td><img src="{animal.image_src}" alt="{animal.name}"></td>
        </tr>
        '''
    html_content += '</tbody></table>'

html_content += '''
</div>

<!-- Bootstrap JS and dependencies -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"
        integrity="sha384-vtPxE0SoKkfUCYn3AP+P6/WmZUq+4HvrW3h3T5Qx1MnFJL7c3fL+9aUjpaACuJjK"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
        integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8sh+Wy2FZhjXtlxyn6Bw8RbOtk7EhVU/dmBoJw"
        crossorigin="anonymous"></script>
</body>
</html>
'''

# Save to a file
with open('collateral_adjectives.html', 'w') as file:
    file.write(html_content)

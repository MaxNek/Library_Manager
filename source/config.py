import os
from itertools import count

SETTINGS_DIR = './settings'
LOCATIONS_FILE = 'locations.txt'
RATING_SCALE_FILE = 'rating_scale.txt'

DEFAULT_RATING_SCALE = ['', '1', '2', '3', '4', '5']

class AppConfig:
    """
    A class to create application settings manager.
    Enables a user to add/delete options for drop-down entry fields.

    Constructor automatically creates (if it doesn't already exist):
     - 'settings' directory.
    """
    def __init__(self):
        if not os.path.exists(SETTINGS_DIR):
            os.mkdir(SETTINGS_DIR)

    def add_book_location(self, new_location: str) -> int:
        """
        Create 'locations.txt' file if it doesn't exist. Add a new book location to the 'locations.txt'.

        :param new_location: String - name of a book location to add.
        :return: Integer - 0 if the location was already in the file. 1 if the location was successfully added.
        """
        location_exists = False
        try:
            with open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='r+') as file:
                locations = file.readlines()
                for location in locations:
                    if location.strip() == new_location:
                        location_exists = True
                        result = 0
                if not location_exists:
                    file.write(f'{new_location}\n')
                    result = 1
        except FileNotFoundError:
            with open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='w') as file:
                file.write(f'{new_location}\n')
                result = 1
        return result

    def remove_book_location(self, location: str) -> int:
        """
        Remove location from the 'locations.txt'.

        :param location: String - name of a book location to remove.
        :return: Integer - 1 if location was successfully removed. 0 - if location was not in the file or the file didn't exist.
        """
        location = f'{location}\n'
        try:
            file =  open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='r')
            locations = file.readlines()
            file.close()
            if location in locations:
                locations.remove(location)
                open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='w').close()
                file = open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='w')
                file.writelines(locations)
                file.close()
                result = 1
            else:
                result = 0
        except FileNotFoundError:
            result = 0
        return result

    def get_book_locations(self) -> list:
        """
        Return a list of all book locations from 'locations.txt' file.
        If the file is empty or doesn't exist, return empty list.

        :return: List - names of book locations or an empty list.
        """
        locations = []
        try:
            with open(f'{SETTINGS_DIR}/{LOCATIONS_FILE}', mode='r') as file:
                for location in file.readlines():
                    locations.append(location.strip())
        except FileNotFoundError:
            locations = []
        return locations

    def set_rating_scale(self, start: int, end: int, step: int | float):
        """
        Write start,end,step in 'rating_scale.txt' file.

        :param start: Integer - minimum rating
        :param end:  Integer - maximum rating
        :param step: Float - step of the scale
        """
        try:
            open(f'{SETTINGS_DIR}/{RATING_SCALE_FILE}', mode='w').close()
            with open(f'{SETTINGS_DIR}/{RATING_SCALE_FILE}', mode='w') as file:
                file.write(f'{start},{end},{step}')
        except FileNotFoundError:
            with open(f'{SETTINGS_DIR}/{RATING_SCALE_FILE}', mode='w') as file:
                file.write(f'{start},{end},{step}')


    def get_rating_scale(self) -> list:
        """
        Return list of rating scale options in ascending order as strings.

        :return: List of rating scale options.
        """
        try:
            with open(f'{SETTINGS_DIR}/{RATING_SCALE_FILE}', mode='r') as file:
                content = file.readline()
                rating_range = content.split(',')
                start = int(rating_range[0])
                stop = int(rating_range[1])
                step = float(rating_range[2])
                rating_scale = ['']
                for i in count(start, step):
                    rating_scale.append(str(i))
                    if i >= stop:
                        break
        except FileNotFoundError:
            rating_scale = DEFAULT_RATING_SCALE
        return rating_scale

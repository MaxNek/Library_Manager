import os

class AppConfig:
    """
    A class to create application configuration manager.
    Enables a user to add/delete options for drop-down entry fields.

    Constructor automatically creates (if it doesn't already exist):
     - 'configuration' directory.
    """
    def __init__(self):
        # check if 'configuration' directory exists and create one if it doesn't.
        if not os.path.exists('configuration'):
            os.mkdir('configuration')

    def add_book_location(self, new_location: str) -> int:
        """
        Create 'locations.txt' file if it doesn't exist. Add a new book location to the 'locations.txt'.

        :param new_location: String - name of a book location to add.
        :return: Integer - 0 if the location was already in the file. 1 if the location was successfully added.
        """
        location_exists = False

        try:
            # Read 'locations.txt' and check if the location is already there.
            # If not write it in the file and set result to 1. If not, set result to 0.
            with open('configuration/locations.txt', mode='r+') as file:
                locations = file.readlines()
                for location in locations:
                    if location.strip() == new_location:
                        location_exists = True
                        result = 0
                if not location_exists:
                    file.write(f'{new_location}\n')
                    result = 1
        except FileNotFoundError:
            # Create 'locations.txt' and write location in it, set result to 1.
            with open('configuration/locations.txt', mode='w') as file:
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
            # Read 'locations.txt'. Check if the location to remove is in the list of locations from the file.
            # If yes, clear the file, re-write it with all locations except the one to remove, set result to 1.
            # If not, set result to 0.
            file =  open('configuration/locations.txt', mode='r')
            locations = file.readlines()
            file.close()
            if location in locations:
                locations.remove(location)
                open('configuration/locations.txt', mode='w').close()
                file = open('configuration/locations.txt', mode='w')
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
            # Read 'locations.txt', strip and append each line to the list of locations.
            with open('configuration/locations.txt', mode='r') as file:
                for location in file.readlines():
                    locations.append(location.strip())
        except FileNotFoundError:
            locations = []
        return locations

    def set_rating_scale(self, rating_scale):
        try:
            open('configuration/rating_scale.txt', mode='w').close()
            with open('configuration/rating_scale.txt', mode='w') as file:
                file.write(f'{range(1, 10)}')
        except FileNotFoundError:
            with open('configuration/rating_scale.txt', mode='w') as file:
                file.write(f'{rating_scale}')


    def get_book_rating_scale(self) -> list:
        try:
            with open('configuration/rating_scale.txt', mode='r') as file:
                content = file.readline()
                rating_scale = content.split(',')
        except FileNotFoundError:
            rating_scale = []
        return rating_scale


conf = AppConfig()

conf.set_rating_scale([1])
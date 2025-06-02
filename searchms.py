import json
import time
import os

"""
The search microservice reads in a text file comprising the search criteria and real estate property listings. 
It filters the real estate property listing based on the given search parameters. If no search parameters are provided,
the microservice returns the entire database.
The results are returned in a separate text file to be picked up by other programs.
"""

def load_request_file(filename):
    """
    Opens the provided request file and reads the search parameters and real estate property data.

    :param filename: Path to the request text file.
                     Line 1 contains JSON search parameters.l
                     Lines 2+ contain a JSON array of property data.
    :return: A tuple containing (search parameters dict, list of dicts comprising RE property records)
    """
    try:
        with open(filename, 'r') as file:
            # Read search parameters from line 1 and RE property data from lines 2 to EOF
            params_line = file.readline()
            data_json = file.read().strip()

            # Parse JSON and return structured data
            params = json.loads(params_line.strip())
            listings = json.loads(data_json)

            return params, listings

    except FileNotFoundError:
        raise FileNotFoundError(f"Request file '{filename}' not found.")
    except json.JSONDecodeError:
        raise ValueError("Request file contains invalid JSON.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading request file: {e}")


def matches_criteria(params, listing):
    """
    Checks whether an RE property listing matches the user's search criteria.

    :param params: Dictionary of search filters including:
        - price_range: [min_price, max_price] or None
        - min_beds: Minimum number of bedrooms (int) or None
        - min_baths: Minimum number of bathrooms (int) or None
        - city: City name (str) or None
    :param listing: Dictionary representing an RE property listing
    :return: True if the listing matches all applicable filters, False otherwise
    """

    price_range = params.get('price_range')
    min_beds = params.get('min_beds')
    min_baths = params.get('min_baths')
    city = params.get('city')

    # Filter by price range, if provided
    if price_range and isinstance(price_range, list):
        min_price, max_price = price_range
        if min_price is not None and listing['price'] < min_price:
            return False
        if max_price is not None and listing['price'] > max_price:
            return False

    # Filter by minimum number of bedrooms, if provided
    if min_beds is not None and listing['bed'] < min_beds:
        return False

    # Filter by minimum number of bathrooms, if provided
    if min_baths is not None and listing['bath'] < min_baths:
        return False

    # Filter by city, if provided
    if city and listing['city'].lower() != city.lower():
        return False

    return True


def filter_listings(params, listings):
    """
    Filters a list of RE property listings based on user-defined search parameters.

    :param params: Dictionary of search filters (e.g., price_range, min_beds, city)
    :param listings: List of RE property dictionaries to evaluate
    :return: List of RE property listings that meet all the specified criteria
    """
    return [listing for listing in listings if matches_criteria(params, listing)]


def write_results(filtered, filename):
    """
    Writes the filtered RE property listings to a text file in JSON format.
    Each line includes: price, bed, bath, city, address, id — separated by commas.

    :param filtered: List of listing dictionaries to write
    :param filename: Path to the output file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(filtered, file, indent=4)     # pretty-print with indentation
    except OSError as e:
        raise OSError(f"Failed to write to output file '{filename}': {e}")


def main():
    """
    Main loop that checks for the request file every 3 seconds.
    If found, processes the search request and writes the results to an output file.
    """

    request_file = 'request.txt'
    result_file = 'results.txt'

    while True:
        if os.path.exists(request_file):
            try:
                # Step 1: Load parameters and data from request file
                params, listings = load_request_file(request_file)

                # Step 2: Filter listings based on search criteria
                filtered = filter_listings(params, listings)

                # Step 3: Write matching results to output file
                write_results(filtered, result_file)

                # Step 4: Delete request file to prevent reprocessing
                os.remove(request_file)

            except Exception as e:
                print(f"Error: {e}")  # Print error to console for debugging

                # Attempt to log error to results file
                try:
                    with open(result_file, 'w') as f:
                        f.write(f"Error processing request: {e}\n")
                except OSError:
                    pass  # Silently ignore file write failures

        # Wait 50 milliseconds before checking again
        time.sleep(0.05)

if __name__ == "__main__":
    main()
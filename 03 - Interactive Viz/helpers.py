import googlemaps
""""
File containing helper methods, factored out to lighten the notebook up
"""

#gmaps = googlemaps.Client('')

def split_and_request(name):
    """
    Most of the university names are of the form 'Long name with many words - LNWMW'.
    For some of them, the request works better with only the first part, and for some
    others with only the second part, thus we try both. Returns None if there is no 
    result.
    """
    uni = name.split(' - ')
    for x in uni:
        r = gmaps.places(x)
        #this isn't right, should be if r['results']
        #however we probably won't use it anymore so might as well leave it
        if r:
            return r
    #no result        
    print(name)
    return None



def canton_from_coordinates(coordinates):
    """
    Using Google Maps Geocode API, more specifically reverse geocoding,
    get the canton code from the raw localisation.
    Throws exception if an object with the wrong format is input. 
    """
    if coordinates is None:
        return None
    response = gmaps.reverse_geocode(coordinates)
    #extract the canton code from the mess
    #it is in the field of type administrative_area_level_1 field
    return next(x for x in response[0]['address_components'] if 'administrative_area_level_1' in x['types'])['short_name']

def extract_lat_lng(row):
    if not row['Raw localisation']['results']:
        return None
    else:
        return row['Raw localisation']['results'][0]['geometry']['location']

def print_index_if_empty(row):
    if not row['Raw localisation']['results']:
        print(row.name)
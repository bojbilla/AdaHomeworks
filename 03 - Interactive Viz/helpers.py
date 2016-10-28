import googlemaps
import folium
from yandex_translate import YandexTranslate
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
        if(r['status'] != 'ZERO_RESULTS'):
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

def get_canton(location):
    if location is None:
        return None
    if next(x for x in location[0]['address_components'] if 'country' in x['types'])['short_name'] == 'CH':
        return next(x for x in location[0]['address_components'] if 'administrative_area_level_1' in x['types'])['short_name']
    return None


def split_and_geocode(name):
    uni = name.split(' - ')
    for x in uni:
        response = gmaps.geocode(x, region='ch')
        if(response):
            return response
    return None

def set_coordinates_and_canton(df, index, lng, lat, canton):
    df.set_value(index, 'Coordinates', {'lng': lng, 'lat': lat})
    df.set_value(index, 'Canton', canton)
    
def create_marker(row, total_canton, total):
    """
    Returns a folium marker at the location of the specified university,
    containing the name of the uni, how much % of canton grants it has and
    how much % of total"""
    location = [row['Coordinates']['lat'], row['Coordinates']['lng']]
    uni = row['University']
    grant = row['Approved Amount']
    percent_canton = "{0:.2f}".format(100*grant/total_canton)
    percent_total = "{0:.2f}".format(100*grant/total)
    return folium.Marker(location = location,
                         popup="Name: "+uni+
                             "\n Percentage of Canton: "+percent_canton+
                             "\n Percentage of total: "+percent_total)
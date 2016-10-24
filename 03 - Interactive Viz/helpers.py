""""
File containing helper methods, factored out to lighten the notebook up
"""

def request_gmaps(name):
    """
    Requests Google maps Places API with the specified name. 
    It adds 'Switzerland' to the query to get more specific results.
    IMPORTANT: 
    Needs a Google API Key to work. This should never be published on github. 
    """
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    payload = {
        'query': name+' Switzerland',
        'key': ''
    }
    return requests.get(url,payload)



def split_and_request(name):
    """
    Most of the university names are of the form 'Long name with many words - LNWMW'.
    For some of them, the request works better with only the first part, and for some
    others with only the second part, thus we try both. Returns None if there is no 
    result.
    """
    uni = name.split(' - ')
    for x in uni:
        r = request_gmaps(x).json()
        if(r['status'] != 'ZERO_RESULTS'):
            return r
            
    print(name)
    return None


def json_2_lat_lon(json):
    """
    Extracts the latitude and the longitude from the result of a request.
    """
    try:
        return json['results'][0]['geometry']['location']
    except:
        print(json)
        return None
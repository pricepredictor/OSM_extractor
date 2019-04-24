import json
import itertools

with open('../geojson-data/spb.geojson') as f:
    city = json.load(f)

with_other_tags = city['features']

with_amenity = [f for f in with_other_tags if 'amenity' in f['properties'].keys()]

relevant_amenities = ['fast_food', 'cafe', 'restaurant', 'nightclub', 'stripclub', 
                 'pub', 'bar', 'courthouse', 'register_office', 'townhall', 
                 'public_building', 'police', 'place_of_worship', 'fountain', 
                 'library', 'theatre', 'clinic', 'hospital', 'bank', 'university',
                 'school', 'cinema']

entries = {a: [] for a in relevant_amenities}
for feature in with_amenity:
    amenity = feature['properties']['amenity']
    if amenity in relevant_amenities:
        entrie = [feature['geometry']['coordinates']]
        if 'name' in feature['properties'].keys():
            entrie.append(feature['properties']['name'])
        entries[amenity].append(entrie)
        
def retreive(tag, value=None): 
    res = [f for f in with_other_tags if tag in f['properties'].keys()]
    if not value is None:
        res = [ f for f in res if f['properties'][tag] == value]
    return res


retrieved = {
    'public_transport': retreive('public_transport'),
    'tram_stop': retreive('railway', 'tram_stop'),
    'subway_station': retreive('station', 'subway'),
    'shop': retreive('shop'),
    'sport_center': retreive('leisure', 'sports_centre'),
    'playground': retreive('leisure', 'playground'),
    'railway': retreive('railway'),
    'office': retreive('office'),
    'monument': retreive('historic', 'monument'),
    'memorial': retreive('historic', 'memorial'),
    'fitness_centre': retreive('leisure', 'fitness_centre'),
    'motel': retreive('tourism', 'motel'),
    'hotel': retreive('tourism', 'hotel'),
    'hostel': retreive('tourism', 'hostel'),
    'artwork': retreive('tourism', 'artwork')
}

for key in retrieved.keys():
    entries[key] = []

    
for key, features in zip(retrieved.keys(), retrieved.values()):
    for feature in features:
        entrie = [feature['geometry']['coordinates']]
        if 'name' in feature['properties'].keys():
            entrie.append(feature['properties']['name'])
        entries[key].append(entrie)
        
with open('../extracted-entries/spb.json', 'w') as fp:
    json.dump(entries, fp)
import yaml

# YAML CONSTANTS
CONFIRM_LIST = ['yes', 'y']
BATHS_LIST = [1, 1.5, 2, 2.5, 3, 3.5, 4]

def get_filters():
    # TODO: Make this compatible with calling program from not root directory
    # TODO: Check if this file exists first as well
    with open('filters.yaml', 'r') as file:
        return yaml.safe_load(file) 
    
def is_valid_filter(filter):
    if filter == None:
        return False
    return filter.strip().lower() in CONFIRM_LIST
    
def validate_baths(baths):
    if baths:
        if baths not in BATHS_LIST:
            if baths < 1:
                baths = 1
            elif baths > 4:
                baths = 4
            baths = round(baths)
    return baths

def validate_beds(min_beds, max_beds):
    if min_beds:
        if min_beds < 0:
            min_beds = 0
        elif min_beds > 4:
            min_beds = 4
    if max_beds:
        if max_beds < 0:
            max_beds = 0
        elif max_beds > 4:
            max_beds = 4
    if min_beds and max_beds:
        if min_beds > max_beds:
            max_beds = min_beds 
    return min_beds, max_beds

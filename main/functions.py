from math import radians, cos, sin, asin, sqrt
from dashboard.models import Info


def hr_to_hm(hr) -> str:
    print(hr)
    delay_hr = int(abs(hr))
    delay_mins = (abs(hr) - delay_hr)*60
    return f"{delay_hr} hr {int(delay_mins)} mins"


def location_validator(lat1, lon1) -> bool:

    info = Info.objects.get(name='main')
    coord_arr = info.geographic_coords.replace(" ", "").split(",")
    radius = info.radius

    lat2 = float(coord_arr[0])
    lon2 = float(coord_arr[1])

    distance = _distance(
        lat1=float(lat1), lon1=float(lon1),
        lat2=lat2, lon2=lon2
    )

    if distance > radius:
        return False
    else:
        return True


def _distance(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c * r)

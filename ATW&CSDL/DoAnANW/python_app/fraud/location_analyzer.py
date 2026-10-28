
import math
from .types import TransactionContext, LocationData
from .constants import CITY_COORDINATES, IMPOSSIBLE_TRAVEL_SPEED_KMH

def get_coords(loc: LocationData) -> dict:
    if loc.latitude is not None and loc.longitude is not None:
        return {"lat": loc.latitude, "lng": loc.longitude}
    city_info = CITY_COORDINATES.get(loc.city)
    if city_info:
        return {"lat": city_info["lat"], "lng": city_info["lng"]}
    return {"lat": 10.8231, "lng": 106.6297}

def calculate_haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def analyze_location(ctx: TransactionContext) -> dict:
    if not ctx.previous_location or not ctx.previous_transaction_time:
        return {
            "location_changed": False,
            "distance_km": 0.0,
            "time_diff_seconds": 0.0,
            "impossible_travel": False,
        }

    location_changed = (
        ctx.previous_location.country != ctx.location.country
        or ctx.previous_location.city != ctx.location.city
    )

    curr_coords = get_coords(ctx.location)
    prev_coords = get_coords(ctx.previous_location)

    distance_km = calculate_haversine_distance_km(
        prev_coords["lat"], prev_coords["lng"], curr_coords["lat"], curr_coords["lng"]
    )

    time_diff_ms = max(1.0, (ctx.timestamp - ctx.previous_transaction_time).total_seconds() * 1000)
    time_diff_seconds = round(time_diff_ms / 1000.0, 1)
    time_diff_hours = time_diff_ms / (1000 * 3600)

    calculated_speed_kmh = distance_km / max(time_diff_hours, 0.0001)
    impossible_travel = distance_km > 50 and calculated_speed_kmh > IMPOSSIBLE_TRAVEL_SPEED_KMH

    return {
        "location_changed": location_changed,
        "distance_km": distance_km,
        "time_diff_seconds": time_diff_seconds,
        "impossible_travel": impossible_travel,
    }


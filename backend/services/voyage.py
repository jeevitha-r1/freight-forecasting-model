from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate approximate straight-line geographic distance
    between two coordinates using the Haversine formula.

    Returns distance in kilometres.
    """

    earth_radius = 6371.0

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1_rad)
        * cos(lat2_rad)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def calculate_voyage(vessel, origin, destination):
    """
    Calculate basic voyage metrics.

    Prototype calculations:
    distance -> time -> fuel -> fuel cost
    """

    # ---------------------------------------------
    # Distance
    # ---------------------------------------------

    distance = calculate_distance(
        origin["latitude"],
        origin["longitude"],
        destination["latitude"],
        destination["longitude"]
    )

    # ---------------------------------------------
    # Voyage time
    # ---------------------------------------------

    voyage_time = distance / vessel["speed"]

    # ---------------------------------------------
    # Fuel required
    # ---------------------------------------------

    fuel_required = (
        vessel["fuel_consumption"]
        * voyage_time
    )

    # ---------------------------------------------
    # Demo fuel price
    # ---------------------------------------------

    fuel_price = 90

    # ---------------------------------------------
    # Fuel cost
    # ---------------------------------------------

    fuel_cost = (
        fuel_required * fuel_price
    )

    return {
        "distance_km": round(distance, 2),
        "voyage_time_hours": round(voyage_time, 2),
        "fuel_required_litres": round(
            fuel_required,
            2
        ),
        "fuel_price_per_litre": fuel_price,
        "estimated_fuel_cost": round(
            fuel_cost,
            2
        )
    }
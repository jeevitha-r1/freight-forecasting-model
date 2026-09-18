import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.voyage import VoyageRequest
from services.compatibility import check_compatibility
from services.voyage import calculate_voyage


# ==================================================
# APPLICATION
# ==================================================

app = FastAPI(
    title="Freight Vessel-Port Optimizer",
    description="SIH Freight Optimization Prototype",
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================
# Allows your Replit frontend to communicate
# with this backend later.
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# DATA FILE PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VESSEL_FILE = os.path.join(
    BASE_DIR,
    "data",
    "vessels.json"
)

PORT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "ports.json"
)


# ==================================================
# LOAD DATA
# ==================================================

with open(VESSEL_FILE, "r", encoding="utf-8") as file:
    vessels = json.load(file)


with open(PORT_FILE, "r", encoding="utf-8") as file:
    ports = json.load(file)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def find_vessel(vessel_id):
    """
    Find vessel using its ID.
    """

    for vessel in vessels:

        if vessel["id"] == vessel_id:
            return vessel

    return None


def find_port(port_id):
    """
    Find port using its ID.
    """

    for port in ports:

        if port["id"] == port_id:
            return port

    return None


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Freight Vessel-Port Optimizer API is running!"
    }


# ==================================================
# VESSELS
# ==================================================

@app.get("/vessels")
def get_vessels():

    return {
        "count": len(vessels),
        "vessels": vessels
    }


# ==================================================
# PORTS
# ==================================================

@app.get("/ports")
def get_ports():

    return {
        "count": len(ports),
        "ports": ports
    }


# ==================================================
# COMPATIBILITY
# ==================================================

@app.post("/compatibility")
def compatibility(request: VoyageRequest):

    vessel = find_vessel(
        request.vessel_id
    )

    origin = find_port(
        request.origin_id
    )

    destination = find_port(
        request.destination_id
    )


    # ----------------------------------------------
    # Validate vessel
    # ----------------------------------------------

    if vessel is None:

        raise HTTPException(
            status_code=404,
            detail="Vessel not found."
        )


    # ----------------------------------------------
    # Validate origin
    # ----------------------------------------------

    if origin is None:

        raise HTTPException(
            status_code=404,
            detail="Origin port not found."
        )


    # ----------------------------------------------
    # Validate destination
    # ----------------------------------------------

    if destination is None:

        raise HTTPException(
            status_code=404,
            detail="Destination port not found."
        )


    # ----------------------------------------------
    # Check compatibility
    # ----------------------------------------------

    origin_result = check_compatibility(
        vessel,
        origin
    )

    destination_result = check_compatibility(
        vessel,
        destination
    )


    overall_compatible = (
        origin_result["compatible"]
        and destination_result["compatible"]
    )


    return {

        "vessel": vessel["name"],

        "origin": origin["name"],

        "destination": destination["name"],

        "compatible": overall_compatible,

        "origin_compatibility": origin_result,

        "destination_compatibility": destination_result
    }


# ==================================================
# COMPLETE VOYAGE CALCULATION
# ==================================================

@app.post("/voyage/calculate")
def calculate_complete_voyage(
    request: VoyageRequest
):

    vessel = find_vessel(
        request.vessel_id
    )

    origin = find_port(
        request.origin_id
    )

    destination = find_port(
        request.destination_id
    )


    # ----------------------------------------------
    # Validation
    # ----------------------------------------------

    if vessel is None:

        raise HTTPException(
            status_code=404,
            detail="Vessel not found."
        )


    if origin is None:

        raise HTTPException(
            status_code=404,
            detail="Origin port not found."
        )


    if destination is None:

        raise HTTPException(
            status_code=404,
            detail="Destination port not found."
        )


    # ----------------------------------------------
    # Compatibility
    # ----------------------------------------------

    origin_compatibility = check_compatibility(
        vessel,
        origin
    )


    destination_compatibility = check_compatibility(
        vessel,
        destination
    )


    overall_compatible = (
        origin_compatibility["compatible"]
        and destination_compatibility["compatible"]
    )


    # ----------------------------------------------
    # Voyage calculations
    # ----------------------------------------------

    voyage = calculate_voyage(
        vessel,
        origin,
        destination
    )


    # ----------------------------------------------
    # Final response
    # ----------------------------------------------

    return {

        "vessel": {
            "id": vessel["id"],
            "name": vessel["name"],
            "type": vessel["vessel_type"],
            "capacity": vessel["capacity"]
        },

        "route": {
            "origin": origin["name"],
            "destination": destination["name"]
        },

        "compatibility": {

            "overall": overall_compatible,

            "origin": origin_compatibility,

            "destination": destination_compatibility
        },

        "voyage": voyage
    }
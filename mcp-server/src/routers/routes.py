from fastapi import APIRouter, HTTPException, Query
import httpx

CITY_COORDINATES = {
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194},
    "San Diego": {"lat": 32.7157, "lon": -117.1611},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Chicago": {"lat": 41.8781, "lon": -87.6298},
    # Add more cities as needed
}

router = APIRouter(
    prefix="/api/v1/mcp",
    tags=["mcp"]
)

@router.get("/weather")
async def get_weather(
    stateCode: str = Query(..., description="State code (e.g., 'CA' for California)"),
    city: str = Query(..., description="City name (e.g., 'Los Angeles')")
):
    """
    Retrieve today's weather from the National Weather Service API based on city and state
    """
    # Get coordinates (latitude, longitude) for the given city
    if city not in CITY_COORDINATES:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found in predefined list. Please use another city."
        )

    coordinates = CITY_COORDINATES[city]
    lat, lon = coordinates["lat"], coordinates["lon"]

    # URL for the NWS API Gridpoints endpoint
    base_url = f"https://api.weather.gov/points/{lat},{lon}"

    try:
        async with httpx.AsyncClient() as client:
            # First, get the gridpoint information for the given location
            gridpoint_response = await client.get(base_url)
            gridpoint_response.raise_for_status()
            gridpoint_data = gridpoint_response.json()

            # Retrieve the forecast data using the gridpoint information
            forecast_url = gridpoint_data["properties"]["forecast"]
            forecast_response = await client.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Returning today's forecast
            today_weather = forecast_data["properties"]["periods"][0]
            return {
                "city": city,
                "state": stateCode,
                "date": today_weather["startTime"],
                "temperature": today_weather["temperature"],
                "temperatureUnit": today_weather["temperatureUnit"],
                "forecast": today_weather["detailedForecast"],
            }
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code = e.response.status_code,
            detail = f"NWS API error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal server error: {str(e)}"
        )
import json
import os
from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def _load_data():
    """Load the carbon footprint data from data.json."""
    data_path = Path(settings.BASE_DIR).parent / 'data.json'
    if not data_path.exists():
        return None
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@api_view(['GET'])
def get_vehicles(request):
    """Return all vehicles with their destinations."""
    data = _load_data()
    if data is None:
        return Response({'error': 'data.json not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(data.get('vehicles', []))


@api_view(['GET'])
def get_vehicle_detail(request, vehicle_id):
    """Return a single vehicle by index."""
    data = _load_data()
    if data is None:
        return Response({'error': 'data.json not found'}, status=status.HTTP_404_NOT_FOUND)
    vehicles = data.get('vehicles', [])
    if vehicle_id < 0 or vehicle_id >= len(vehicles):
        return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(vehicles[vehicle_id])


@api_view(['GET'])
def get_summary(request):
    """Return aggregated carbon footprint summary."""
    data = _load_data()
    if data is None:
        return Response({'error': 'data.json not found'}, status=status.HTTP_404_NOT_FOUND)

    vehicles = data.get('vehicles', [])
    total_co2 = 0
    total_distance = 0
    total_fuel = 0
    total_destinations = 0

    for v in vehicles:
        for d in v.get('destinations', []):
            total_co2 += d.get('co2Emissions', 0)
            total_distance += d.get('roundTripDistance', 0)
            total_fuel += d.get('fuelUsed', 0)
            total_destinations += 1

    return Response({
        'totalVehicles': len(vehicles),
        'totalDestinations': total_destinations,
        'totalCo2Kg': round(total_co2, 2),
        'totalDistanceKm': round(total_distance, 2),
        'totalFuelLiters': round(total_fuel, 2),
        'exportDate': data.get('exportDate', ''),
    })

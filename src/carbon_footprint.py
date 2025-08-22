import googlemaps
from datetime import datetime
from typing import Optional
import os

# Google Maps API Key - should be loaded from environment variable for security
GOOGLE_MAPS_API_KEY = "AIzaSyA5lNc_aRFIbnbYPMHczI6R1MF7jPuAZLw"


def get_driving_distance_km(api_key: str, address1: str, address2: str) -> float | None:
    """
    Calculates the driving distance in kilometers between two addresses
    using the Google Maps Directions API.

    Args:
        api_key: Your Google Maps API key.
        address1: The starting address as a string.
        address2: The destination address as a string.

    Returns:
        The driving distance in kilometers as a float, or None if a route
        cannot be found or an error occurs.
    """
    # Initialize the Google Maps client
    try:
        gmaps = googlemaps.Client(key=api_key)

        # Request driving directions
        # 'now' can be used to get traffic-dependent routing
        now = datetime.now()
        directions_result = gmaps.directions(address1,
                                             address2,
                                             mode="driving",
                                             departure_time=now)

        # Check if a route was found
        if not directions_result:
            print(f"Error: No driving route found between '{address1}' and '{address2}'.")
            return None

        # The result is a list of routes. We'll take the first one.
        # The distance is in the 'legs' of the route and is given in meters.
        distance_in_meters = directions_result[0]['legs'][0]['distance']['value']
        
        # Convert meters to kilometers
        distance_in_km = distance_in_meters / 1000
        
        return distance_in_km

    except googlemaps.exceptions.ApiError as e:
        print(f"API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def validate_and_suggest_address(gmaps_client, address: str) -> tuple[bool, str, str]:
    """
    Validate an address and suggest improvements if needed.
    
    Returns:
        (is_valid, validated_address, suggestion_message)
    """
    if not address or not address.strip():
        return False, "", "Adresse vide"
    
    try:
        geocode_result = gmaps_client.geocode(address)
        if geocode_result:
            # Get the formatted address from Google
            formatted_address = geocode_result[0]['formatted_address']
            return True, formatted_address, "Adresse valide"
        else:
            # Try to suggest improvements
            suggestions = []
            address_lower = address.lower()
            
            if "france" not in address_lower:
                suggestions.append("Ajouter ', France' à la fin")
            if not any(char.isdigit() for char in address):
                suggestions.append("Ajouter un numéro de rue")
            if len(address.split()) < 3:
                suggestions.append("Adresse trop courte, ajouter plus de détails")
                
            suggestion_msg = "Adresse non trouvée. Suggestions: " + "; ".join(suggestions) if suggestions else "Adresse non trouvée"
            return False, address, suggestion_msg
            
    except Exception as e:
        return False, address, f"Erreur de validation: {str(e)}"


def calculate_carbon_footprint_km(sondeur_address: str, chantier_address: str, days: int) -> Optional[float]:
    """
    Calculate the total carbon footprint distance for an affectation.
    
    Formula: driving_distance * 2 (round trip) * days
    
    Args:
        sondeur_address: Address of the sondeur
        chantier_address: Address of the chantier
        days: Number of days for the affectation
        
    Returns:
        Total distance in kilometers, or None if calculation fails
    """
    if not sondeur_address or not chantier_address or days <= 0:
        return None
        
    # Get the one-way driving distance
    one_way_distance = get_driving_distance_km(
        GOOGLE_MAPS_API_KEY, 
        sondeur_address, 
        chantier_address
    )
    
    if one_way_distance is None:
        return None
    
    # Calculate total distance: one_way * 2 (round trip) * days
    total_distance = one_way_distance * 2 * days
    
    return total_distance


def calculate_co2_emissions(distance_km: float, emission_factor: float = 0.120) -> float:
    """
    Calculate CO2 emissions based on distance.
    
    Args:
        distance_km: Total distance in kilometers
        emission_factor: CO2 emission factor in kg/km (default: 0.120 kg/km for average car)
        
    Returns:
        CO2 emissions in kg
    """
    return distance_km * emission_factor


class CarbonFootprintCalculator:
    """Class to handle carbon footprint calculations for the application"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GOOGLE_MAPS_API_KEY
    
    def calculate_affectation_footprint(self, sondeur_address: str, chantier_address: str, days: int) -> dict:
        """
        Calculate complete carbon footprint data for an affectation.
        
        Returns:
            Dictionary with distance_km, co2_kg, and calculation details
        """
        result = {
            'distance_km': None,
            'co2_kg': None,
            'one_way_distance': None,
            'round_trip_distance': None,
            'days': days,
            'error': None
        }
        
        # Validate inputs
        if not sondeur_address or not sondeur_address.strip():
            result['error'] = "Adresse du sondeur manquante ou vide"
            return result
            
        if not chantier_address or not chantier_address.strip():
            result['error'] = "Adresse du chantier manquante ou vide"
            return result
            
        if days <= 0:
            result['error'] = "Le nombre de jours doit être supérieur à 0"
            return result
        
        try:
            print(f"\n🌍 Calcul d'empreinte carbone:")
            print(f"   Sondeur: {sondeur_address}")
            print(f"   Chantier: {chantier_address}")
            print(f"   Jours: {days}")
            
            # Try to initialize Google Maps client for validation
            try:
                gmaps = googlemaps.Client(key=self.api_key)
                
                # Validate addresses first
                sondeur_valid, sondeur_formatted, sondeur_msg = validate_and_suggest_address(gmaps, sondeur_address)
                chantier_valid, chantier_formatted, chantier_msg = validate_and_suggest_address(gmaps, chantier_address)
                
                print(f"   Validation sondeur: {sondeur_msg}")
                print(f"   Validation chantier: {chantier_msg}")
                
                if not sondeur_valid:
                    result['error'] = f"Adresse sondeur invalide: {sondeur_msg}"
                    return result
                    
                if not chantier_valid:
                    result['error'] = f"Adresse chantier invalide: {chantier_msg}"
                    return result
                    
                # Use validated addresses
                from_address = sondeur_formatted
                to_address = chantier_formatted
                
            except Exception as api_error:
                # API unavailable, use original addresses
                print(f"   API validation unavailable: {api_error}")
                print("   Proceeding with original addresses...")
                from_address = sondeur_address.strip()
                to_address = chantier_address.strip()
            
            # Get one-way distance using addresses
            one_way_distance = get_driving_distance_km(
                self.api_key, 
                from_address, 
                to_address
            )
            
            if one_way_distance is None:
                result['error'] = "Impossible de calculer la distance. Vérifiez que les adresses sont correctes et complètes."
                return result
            
            # Calculate total distance
            round_trip_distance = one_way_distance * 2
            total_distance = round_trip_distance * days
            
            # Calculate CO2 emissions
            co2_emissions = calculate_co2_emissions(total_distance)
            
            result.update({
                'distance_km': total_distance,
                'co2_kg': co2_emissions,
                'one_way_distance': one_way_distance,
                'round_trip_distance': round_trip_distance
            })
            
        except Exception as e:
            result['error'] = f"Erreur lors du calcul: {str(e)}"
        
        return result
    
    def get_summary_by_sondeur(self, session) -> dict:
        """
        Calculate carbon footprint summary grouped by sondeur.
        
        Args:
            session: SQLAlchemy database session
            
        Returns:
            Dictionary with totals per sondeur and overall total
        """
        from src.models import UniteTravail, Sondeur
        
        # Get all affectations with calculated distances
        affectations = session.query(UniteTravail).filter(
            UniteTravail.distance_km.isnot(None)
        ).all()
        
        summary = {}
        total_distance = 0
        total_co2 = 0
        
        for affectation in affectations:
            sondeur_name = affectation.sondeur.name if affectation.sondeur else "Non assigné"
            
            if sondeur_name not in summary:
                summary[sondeur_name] = {
                    'total_distance_km': 0,
                    'total_co2_kg': 0,
                    'affectations_count': 0
                }
            
            distance = affectation.distance_km or 0
            co2 = calculate_co2_emissions(distance)
            
            summary[sondeur_name]['total_distance_km'] += distance
            summary[sondeur_name]['total_co2_kg'] += co2
            summary[sondeur_name]['affectations_count'] += 1
            
            total_distance += distance
            total_co2 += co2
        
        return {
            'by_sondeur': summary,
            'totals': {
                'total_distance_km': total_distance,
                'total_co2_kg': total_co2,
                'total_affectations': len(affectations)
            }
        }

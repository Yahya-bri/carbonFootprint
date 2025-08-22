#!/usr/bin/env python3
"""
Test script to debug carbon footprint calculation with better error handling
"""

from src.carbon_footprint import CarbonFootprintCalculator

def test_carbon_footprint_debug():
    """Test carbon footprint calculation with debug info"""
    
    calculator = CarbonFootprintCalculator()
    
    # Test cases - mix of valid and invalid addresses
    test_cases = [
        {
            "name": "Valid French addresses",
            "sondeur": "1 Rue de Rivoli, 75001 Paris, France",
            "chantier": "Tour Eiffel, 5 Avenue Anatole France, 75007 Paris, France",
            "days": 3
        },
        {
            "name": "Original test addresses",
            "sondeur": "64 Rue paul louis lande 33000 Bordeaux",
            "chantier": "280 Avenue du compte vert 73000 Chambery",
            "days": 5
        },
        {
            "name": "Invalid address test",
            "sondeur": "Invalid Address 123",
            "chantier": "Another Invalid Address XYZ",
            "days": 2
        },
        {
            "name": "Empty address test",
            "sondeur": "",
            "chantier": "Valid Address, Paris, France",
            "days": 1
        }
    ]
    
    print("🧪 Test de calcul d'empreinte carbone avec gestion d'erreurs améliorée")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        result = calculator.calculate_affectation_footprint(
            test_case['sondeur'], 
            test_case['chantier'], 
            test_case['days']
        )
        
        if result['error']:
            print(f"❌ Erreur: {result['error']}")
        else:
            print(f"✅ Succès!")
            print(f"   Distance aller simple: {result['one_way_distance']:.2f} km")
            print(f"   Distance aller-retour: {result['round_trip_distance']:.2f} km")
            print(f"   Distance totale ({result['days']} jours): {result['distance_km']:.2f} km")
            print(f"   Émissions CO₂: {result['co2_kg']:.2f} kg")
        
        print("-" * 50)

if __name__ == "__main__":
    test_carbon_footprint_debug()

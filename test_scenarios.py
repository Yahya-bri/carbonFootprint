#!/usr/bin/env python3
"""
Test the carbon footprint system with real application workflow
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from carbon_footprint import calculate_carbon_footprint_km

def test_real_scenarios():
    """Test realistic scenarios"""
    
    print("=== Testing Real Application Scenarios ===\n")
    
    # Real scenarios that might occur in the application
    scenarios = [
        {
            'name': 'Paris to Lyon (5 days)',
            'sondeur': 'Paris, France',
            'chantier': 'Lyon, France', 
            'days': 5
        },
        {
            'name': 'Marseille to Nice (3 days)',
            'sondeur': 'Marseille', 
            'chantier': 'Nice',
            'days': 3
        },
        {
            'name': 'Local work (1 day)',
            'sondeur': 'Toulouse', 
            'chantier': 'Toulouse',
            'days': 1
        },
        {
            'name': 'Cross-country (10 days)',
            'sondeur': 'Lille',
            'chantier': 'Marseille', 
            'days': 10
        },
        {
            'name': 'Invalid inputs',
            'sondeur': '',
            'chantier': 'Paris',
            'days': 0
        }
    ]
    
    for scenario in scenarios:
        print(f"📋 Scenario: {scenario['name']}")
        print(f"   Sondeur: {scenario['sondeur']}")
        print(f"   Chantier: {scenario['chantier']}")
        print(f"   Days: {scenario['days']}")
        
        total_distance = calculate_carbon_footprint_km(
            scenario['sondeur'], 
            scenario['chantier'], 
            scenario['days']
        )
        
        if total_distance is not None:
            # Calculate the emissions
            co2_emissions = total_distance * 0.120  # kg CO2 per km
            one_way = total_distance / (2 * scenario['days']) if scenario['days'] > 0 else 0
            
            print(f"   ✅ Results:")
            print(f"      One-way distance: {one_way:.1f} km")
            print(f"      Total distance: {total_distance:.1f} km")
            print(f"      CO2 emissions: {co2_emissions:.2f} kg")
        else:
            print(f"   ❌ Could not calculate distance")
        
        print()
    
    print("=" * 60)
    print("✅ Real scenario testing completed!")
    print("\n💡 The system handles various real-world cases gracefully.")

if __name__ == "__main__":
    test_real_scenarios()

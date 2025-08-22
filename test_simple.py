#!/usr/bin/env python3
"""
Test the simplified carbon footprint system
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from carbon_footprint import get_driving_distance_km, calculate_carbon_footprint_km, CarbonFootprintCalculator

def test_simplified_system():
    """Test the simplified carbon footprint system"""
    
    print("=== Testing Simplified Carbon Footprint System ===\n")
    
    # Test 1: Direct function call
    print("1. Testing get_driving_distance_km:")
    print("-" * 40)
    
    result = get_driving_distance_km("test_key", "Paris", "Lyon")
    if result is None:
        print("✅ Function correctly returns None for invalid API key")
    else:
        print(f"❌ Unexpected result: {result}")
    
    # Test 2: Carbon footprint calculation
    print("\n2. Testing calculate_carbon_footprint_km:")
    print("-" * 40)
    
    result = calculate_carbon_footprint_km("Paris", "Lyon", 3)
    if result is None:
        print("✅ Function correctly returns None when API is unavailable")
    else:
        print(f"❌ Unexpected result: {result}")
    
    # Test 3: Calculator class
    print("\n3. Testing CarbonFootprintCalculator:")
    print("-" * 40)
    
    calculator = CarbonFootprintCalculator("test_key")
    result = calculator.calculate_affectation_footprint("Paris", "Lyon", 3)
    
    if result.get('error'):
        print(f"✅ Calculator correctly handles error: {result['error']}")
    else:
        print(f"❌ Unexpected result: {result}")
    
    print("\n" + "=" * 60)
    print("✅ Simplified system test completed!")
    print("\n💡 The system now uses the simple Google Maps API function.")
    print("💡 When a valid API key is provided, it will return actual distances.")

if __name__ == "__main__":
    test_simplified_system()

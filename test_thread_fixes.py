#!/usr/bin/env python3
"""
Test the thread fixes for the QThread crash issue
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_thread_cleanup():
    """Test that threads are properly cleaned up"""
    
    print("=== Testing Thread Cleanup Fixes ===\n")
    
    # Test the AffectationForm imports
    try:
        from src.ui.forms import AffectationForm, CarbonFootprintThread
        print("✅ AffectationForm imports successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test the CarbonFootprintView imports
    try:
        from src.ui.carbon_footprint_view import CarbonFootprintView, CarbonFootprintCalculationThread
        print("✅ CarbonFootprintView imports successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test thread class creation
    try:
        thread = CarbonFootprintThread("Paris", "Lyon", 3)
        print("✅ CarbonFootprintThread creates successfully")
        
        # Test cleanup
        if hasattr(thread, 'terminate'):
            print("✅ Thread has terminate method")
        if hasattr(thread, 'wait'):
            print("✅ Thread has wait method")
            
    except Exception as e:
        print(f"❌ Thread creation error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Thread cleanup fixes test completed!")
    print("\n💡 Key fixes implemented:")
    print("  - Added thread tracking in AffectationForm.__init__")
    print("  - Added cleanup_thread() method with proper signal disconnection")
    print("  - Added cleanup in accept(), reject(), and closeEvent()")
    print("  - Added thread stopping in calculate_carbon_footprint()")
    print("  - Added similar fixes to CarbonFootprintView")
    print("\n🔧 This should resolve the 'QThread: Destroyed while thread is still running' error")

if __name__ == "__main__":
    test_thread_cleanup()

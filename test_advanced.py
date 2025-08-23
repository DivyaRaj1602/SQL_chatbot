#!/usr/bin/env python3
"""
Test the new Advanced SQL Pipeline
"""

from advanced_pipeline import AdvancedSQLPipeline

def test_advanced_pipeline():
    """Test if the advanced pipeline can handle complex queries"""
    print("🧪 Testing Advanced SQL Pipeline...")
    
    try:
        # Initialize the pipeline
        pipeline = AdvancedSQLPipeline()
        print("✅ Pipeline initialized successfully!")
        
        # Test a simple query
        print("\n📝 Testing simple query...")
        result = pipeline.process_query("Show me all employees")
        if result['success']:
            print(f"✅ Simple query works! Found {result['result_count']} rows")
        else:
            print(f"❌ Simple query failed: {result['error']}")
        
        # Test a JOIN query
        print("\n📝 Testing JOIN query...")
        result = pipeline.process_query("Get me orders with customer names")
        if result['success']:
            print(f"✅ JOIN query works! Found {result['result_count']} rows")
            print(f"🎯 Tables involved: {result['target_table']}")
        else:
            print(f"❌ JOIN query failed: {result['error']}")
        
        # Test schema display
        print("\n📊 Testing schema display...")
        pipeline.show_schema()
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_advanced_pipeline()

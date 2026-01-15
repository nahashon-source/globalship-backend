"""
Simple API test script to verify endpoints are working.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint."""
    response = requests.get("http://localhost:8000/health")
    print(f"Health Check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_register():
    """Test user registration."""
    data = {
        "email": "test@globalship.com",
        "password": "Test123456",
        "company_name": "Test Company",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"\nRegister User: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code in [200, 201]

def test_login():
    """Test user login."""
    data = {
        "email": "test@globalship.com",
        "password": "Test123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"\nLogin User: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if response.status_code == 200:
        return result.get("access_token")
    return None

def test_get_me(token):
    """Test get current user."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"\nGet Current User: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_create_shipment(token):
    """Test create shipment."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "origin_city": "Nairobi",
        "origin_country": "Kenya",
        "destination_city": "Dar es Salaam",
        "destination_country": "Tanzania",
        "service_type": "air",
        "weight": 25.5,
        "package_count": 2
    }
    response = requests.post(f"{BASE_URL}/shipments/", json=data, headers=headers)
    print(f"\nCreate Shipment: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if response.status_code in [200, 201]:
        return result.get("tracking_number")
    return None

def test_track_shipment(tracking_number):
    """Test public tracking endpoint."""
    response = requests.get(f"{BASE_URL}/shipments/track/{tracking_number}")
    print(f"\nTrack Shipment: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_dashboard(token):
    """Test dashboard stats."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print(f"\nDashboard Stats: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("GlobalShip API Tests")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed! Make sure the API is running.")
        return
    
    # Test registration
    test_register()
    
    # Test login
    token = test_login()
    if not token:
        print("\n❌ Login failed!")
        return
    
    print(f"\n✅ Got access token: {token[:20]}...")
    
    # Test authenticated endpoints
    test_get_me(token)
    
    # Test shipment creation
    tracking_number = test_create_shipment(token)
    
    if tracking_number:
        print(f"\n✅ Created shipment: {tracking_number}")
        # Test public tracking
        test_track_shipment(tracking_number)
    
    # Test dashboard
    test_dashboard(token)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

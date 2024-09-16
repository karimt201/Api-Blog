from app import app  

def test_home_route():
    with app.test_client() as client:  
        response = client.get('/home')  
        return response  

s = test_home_route() 
print(s.status_code)  
print(s.data)  

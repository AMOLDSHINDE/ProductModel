import json
import os
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from .models import ProductModel
from rest_framework import status
from .serializers import ProductSerializers

DUMMY_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy_data.json')

def load_dummy_data():
    try:
        with open(DUMMY_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {DUMMY_DATA_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {DUMMY_DATA_FILE}")
        return []

def save_dummy_data(data):
    try:
        with open(DUMMY_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# @csrf_exempt
@api_view(["POST"])
def create_product(request):
    try:
        if request.method == "POST":
            bytes_data = request.body  # byte data
            print(f"Received byte data: {bytes_data}")
            my_json = bytes_data.decode('utf8').replace("'", '"')  # bytes to json data
            print(f"Decoded JSON string: {my_json}")
            python_dict = json.loads(my_json)
            print(f"Converted to Python dict: {python_dict}")
            ser = ProductSerializers(data=python_dict)
            if ser.is_valid():
                data = ser.save()
                
                # Load existing dummy data
                dummy_data = load_dummy_data()
                
                # Append the new product data
                new_product = {
                    "name": data.name,
                    "price": data.price,
                    "retailer_name": data.retailer_name
                }
                dummy_data.append(new_product)

                # Save updated dummy data
                save_dummy_data(dummy_data)

                success_msg = {'msg': f'data Insert successfully. data:{data.__dict__}'}
                json_data = json.dumps(success_msg)
                return HttpResponse(json_data, status=status.HTTP_201_CREATED, content_type='application/json')
            else:
                error_msg = {'msg': 'Invalid json data', 'errors': ser.errors}
                json_data = json.dumps(error_msg)
                return HttpResponse(json_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        error_msg = {'msg': 'Invalid JSON format'}
        json_data = json.dumps(error_msg)
        return HttpResponse(json_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_msg = {'msg': 'An error occurred: ' + str(e)}
        json_data = json.dumps(error_msg)
        return HttpResponse(json_data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def search_products(request, name):
    try:
        if not name:
            return HttpResponse(
                json.dumps({"msg": "Product name is required"}), 
                status=status.HTTP_400_BAD_REQUEST, 
                content_type='application/json'
            )
        
        dummy_data = load_dummy_data()
        consolidated_data = []

        for product in dummy_data:
            if name.lower() in product['name'].lower():
                consolidated_data.append({
                    # "store": product['store'],
                    "name": product['name'],
                    "price": product['price'],
                    "retailer_name": product['retailer_name']
                })

        if not consolidated_data:
            return HttpResponse(
                json.dumps({"msg": "No products found"}), 
                status=status.HTTP_404_NOT_FOUND, 
                content_type='application/json'
            )

        return HttpResponse(
            json.dumps(consolidated_data), 
            status=status.HTTP_200_OK, 
            content_type='application/json'
        )

    except Exception as e:
        error_msg = {'msg': 'An error occurred: ' + str(e)}
        json_data = json.dumps(error_msg)
        return HttpResponse(
            json_data, 
            content_type='application/json', 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from rest_framework import viewsets
class ProductModelviewset(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializers


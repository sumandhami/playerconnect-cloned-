from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from backend.futsal_be.kick.utilities.utilities_admin import get_all_players,signup_u,add_futsal,input_timeslotbyFutsal
from backend.futsal_be.kick.utilities.utilities_admin import update_game_status
import json

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"message": "CSRF token set!"})

# Create your views here.
def members(request):
    return HttpResponse("Hello World")

def player_list(request): 
    players = get_all_players()
    return JsonResponse({"players": players})

def signup(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            location = data.get("location")
            phone_number = data.get("phone_number")

            # Validate inputs
            if not all([name, email, password, location, phone_number]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})

            # Call the add_user function
            result = signup_u(name, email, password, location, phone_number)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
        
def addfutsal(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            name = data.get("name")
            location = data.get("location")
            google_map_location = data.get("google_map_location")
            longitude = data.get("longitude")
            latitude = data.get("latitude")
            phone_number = data.get("phone_number")
            # Validate inputs
            if not all([name, location,google_map_location,longitude,latitude,phone_number]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})

            # Call the add_user function
            result = add_futsal(name, location,google_map_location,longitude,latitude,phone_number)
            return JsonResponse(result)
            ...
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
        
def addtimeSlotbyFutsal(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            futsal_id = data.get("futsal_id")
            date= data.get("date")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            state = data.get("state")
            occupied_by= data.get("occupied_by")

            if not all([futsal_id,date,start_time,end_time,state]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})
            
            result = input_timeslotbyFutsal(futsal_id,date,start_time,end_time,state,occupied_by)
            return JsonResponse(result)
            ...
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
        


def complete_game_request(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            request_id = data.get("request_id")

            # Validate input
            if not request_id:
                return JsonResponse({"status": "error", "message": "Request ID is required!"})

            # Call utility function to update game status
            result = update_game_status(request_id)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {e}"})

    return JsonResponse({"status": "error", "message": "Invalid request method. Use POST."})





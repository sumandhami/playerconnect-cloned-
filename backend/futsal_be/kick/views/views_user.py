from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from backend.futsal_be.kick.middleware import checkAuth
from backend.futsal_be.kick.utilities.utilities_user import pick_slot,create_participation_request,handle_participation
from backend.futsal_be.kick.utilities.utilities_user import change_state,login_u
from backend.futsal_be.kick.utilities.haversine import calculate_dist
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Check if email and password are provided
            if not email or not password:
                return JsonResponse({"status": "error", "message": "Email and password are required."}, status=400)

            # Call the login function
            result = login_u(email, password)

            # Return the result of the login attempt
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"}, status=400)
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error during login: {e}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred. Please try again later."}, status=500)


def Change_state(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            
            result = change_state(user_id)
            return JsonResponse(result)
        
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})

#@checkAuth
def pick_time_slot(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            slot_id = data.get("slot_id")
            user_id = data.get("user_id")
            player_count = data.get("player_count")

            # Validate input
            if not all([slot_id, user_id, player_count]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})

            # Call utility function to pick slot
            result = pick_slot(slot_id, user_id, player_count)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {e}"})

    return JsonResponse({"status": "error", "message": "Invalid request method. Use POST."})

def join_request(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            request_id = data.get("request_id")
            user_id = data.get("user_id")

            # Validate input
            if not all([request_id, user_id]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})
            
            result = create_participation_request(request_id,user_id)
            return JsonResponse(result)
            ...
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})

def handleparticiation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request_id = data.get("request_id")
            user_id = data.get("user_id")
            action = data.get("action")
    

            if not all([request_id,user_id,action ]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})
            
            result = handle_participation(request_id,user_id,action)
            return JsonResponse(result)
            ...
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})

def near_by(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            longitude = data.get("longitude")
            latitude = data.get("latitude")
            if not all([longitude,latitude]):
                return JsonResponse({"status": "error", "message": "All fields are required!"})
            result = calculate_dist((longitude,latitude))
            print(result)
            return JsonResponse(result)
            pass
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
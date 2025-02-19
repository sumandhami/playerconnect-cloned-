from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from backend.futsal_be.kick.middleware import checkAuth
from backend.futsal_be.kick.utilities.utilities_user import pick_slot,create_participation_request,handle_participation
from backend.futsal_be.kick.utilities.utilities_user import change_state,login_u,update_u,getplayer_u
from backend.futsal_be.kick.utilities.haversine import calculate_dist
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from backend.futsal_be.kick.authenticate.checkjwt import decryptToken


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
        
def getplayer(request):
    if request.method == "GET":
        token = request.headers.get('Authorization', '').split(' ')[1]  # 'Bearer <token>'
        try:
            user_id_dict = decryptToken(token)
            user_id = user_id_dict['user_id']

            result = getplayer_u(user_id)
            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    pass
        
#@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this view
def update(request):
    if request.method == "POST":
        token = request.headers.get('Authorization', '').split(' ')[1]  # 'Bearer <token>'
        try:
            user_id_dict = decryptToken(token)
            user_id = user_id_dict['user_id']
            
            name = request.POST.get("name")  # Use request.POST instead of json.loads
            location = request.POST.get("location")
            phone_number = request.POST.get("phone_number")
            image = request.FILES.get("image")  # Get the uploaded file

            image_url = None

            if image:
                # Save image in media/profile_pics/
                image_filename = f"profile_{user_id}.jpg"  # Unique filename
                image_path = os.path.join("profile_pics", image_filename)  # Relative path
                full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)  # Full path

                # Save the image to disk
                default_storage.save(full_image_path, ContentFile(image.read()))

                # Create URL for the image
                image_url = f"{settings.MEDIA_URL}{image_path}"

            # Call function to update user (store image_url instead of binary data)
            result = update_u(user_id, name, image_url, location, phone_number)

            return JsonResponse({"status": "success", "image": image_url})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def Change_state(request):
    if request.method == "POST":
        token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            user_id_dict = decryptToken(token)
            user_id = user_id_dict['user_id']
            
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
            return JsonResponse({"data":result})
            pass
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data!"})
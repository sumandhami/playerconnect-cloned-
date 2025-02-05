import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import bcrypt
from sqlalchemy.exc import IntegrityError
from backend.futsal_be.futsal_be.db_setup import Session_local
from backend.futsal_be.kick.createToken import genToken
from kick.models import User,FutsalLocation,TimeSlot,GameRequest,PlayerParticipation
from sqlalchemy import text

def get_session():
    return Session_local()

def login_u(email, password):
    session = get_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        
        if not user:
            return {"status": "error", "message": "Signup first"}
        
        # Check if the password is correct
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = genToken(user.user_id)  # Generate a JWT token
            return {
                "status": "success", 
                "message": "Login successful", 
                "token": token
            }
        else:
            return {"status": "error", "message": "Incorrect password"}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": "An error occurred. Please try again later."}
    finally:
        session.close()
    

def change_state(user_id):
    session = get_session()
    try:
        user = session.query(User).filter_by(user_id = user_id).first()
        if not user:
            return {"status": "error", "message": "User not found!"}
        
        if user.status == "available":
            user.status = "not available"
        else:
            user.status = "available"
        
        session.commit()

        return {"status": "success", "message": f"{user_id} status is toggle."}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"An error occurred: {e}"}
    
    finally:
        session.close()

def pick_slot(slot_id, user_id, player_count):
    session = get_session()
    try:
        # Fetch the slot
        slot = session.query(TimeSlot).filter_by(slot_id=slot_id).first()
        if not slot:
            return {"status": "error", "message": "Time slot not found!"}

        # Check if the slot is available
        if slot.state != "available":
            return {"status": "error", "message": "Time slot is not available!"}

        # Update the slot state and occupied_by field
        slot.state = "occupied"
        slot.occupied_by = user_id

        # Create a game request
        game_request = GameRequest(
            slot_id=slot_id,
            created_by=user_id,
            player_count=player_count,
            status="open"
        )
        session.add(game_request)
        session.commit()

        return {"status": "success", "message": f"Slot {slot_id} picked by user {user_id}."}

    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "Database integrity error!"}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"An error occurred: {e}"}

    finally:
        session.close()

def update_game_status(request_id):
    session = get_session()
    try:
        # Fetch the game request
        game_request = session.query(GameRequest).filter_by(request_id=request_id).first()
        if not game_request:
            return {"status": "error", "message": "Game request not found!"}

        # Fetch the slot
        slot = session.query(TimeSlot).filter_by(slot_id=game_request.slot_id).first()
        if not slot:
            return {"status": "error", "message": "Associated time slot not found!"}

        # Check player count and update statuses
        if game_request.player_count >= 9:
            game_request.status = "completed"
            slot.state = "booked"

        session.commit()

        return {"status": "success", "message": "Game request and slot updated successfully."}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"An error occurred: {e}"}

    finally:
        session.close()

def create_participation_request(request_id, user_id):
    session = get_session()
    try:
        # Check if the game request exists
        game_request = session.query(GameRequest).filter_by(request_id=request_id).first()
        if not game_request:
            return {"status": "error", "message": "Game request not found!"}

        # Create a participation record
        participation = PlayerParticipation(
            request_id=request_id,
            user_id=user_id,
            status="pending"
        )
        session.add(participation)
        session.commit()
        return {"status": "success", "message": "Participation request created successfully."}

    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "Participation request already exists!"}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"An error occurred: {e}"}

    finally:
        session.close()

def handle_participation(request_id, user_id, action):
    session = get_session()
    try:
        # Fetch the game request
        game_request = session.query(GameRequest).filter_by(request_id=request_id).first()
        if not game_request:
            return {"status": "error", "message": "Game request not found!"}

        # Fetch the participation record
        participation = session.query(PlayerParticipation).filter_by(request_id=request_id, user_id=user_id).first()
        if not participation:
            return {"status": "error", "message": "Participation record not found!"}

        if action == "confirm":
            participation.status = "confirmed"
            game_request.player_count += 1
            if game_request.player_count >= 9:
                update_game_status(request_id)

        elif action == "cancel":
            participation.status = "cancelled"

        session.commit()
        return {"status": "success", "message": f"Participation {action}ed successfully."}

    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"An error occurred: {e}"}

    finally:
        session.close()

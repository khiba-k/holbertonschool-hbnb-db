from Model.place import Place
from Model.review import Review
from flask_jwt_extended import JWTManager, get_jwt_identity, get_current_user, jwt_required, get_jwt
from create_app_db import db

def user_permission(view, user_id=None, data=None):
    claims = get_jwt()
    role = claims.get("roles")
    jwt_id = get_jwt_identity()

    if "admin" in role or jwt_id == user_id:

        if user_id is None:
            return view()
        elif data is None:
            return view(user_id)
        return view(user_id, data)
    return "Unauthorized", 403

def place_permission(view, place_id=None, data=None):
    claims = get_jwt()
    role = claims.get("roles")
    jwt_id = get_jwt_identity()

    if place_id is None:
        if data is None:
            return view()
        return view(data)
    
    filter_place = db.session.query(Place).filter_by(place_id=place_id).first()
    if filter_place is None:
        return "Place not found", 404
    
    user_id = filter_place.host_id
    
    if "admin" in role or jwt_id == user_id:
        if data is None:
            return view(place_id)
        return view(data, place_id)
    return "Unauthorized", 403

def review_permission(view, place_id=None, data=None, user_id=None, review_id=None):
    claims = get_jwt()
    role = claims.get("roles")
    jwt_id = get_jwt_identity()

    if user_id is None:
        if data is None:
            if place_id is None:
                return view(review_id)
            return view(place_id)
        return view(data, place_id)
    
    if review_id is not None:
        filter_review = db.session.query(Review).filter_by(review_id=review_id).first()
        if filter_review is None:
            return "Review not found", 404

        reviewer_id = filter_review.user_id

        if "admin" in role or jwt_id == reviewer_id:
            if place_id is None:
                if review_id is None:
                    return view(data, user_id)
                if data is None:
                    return view(review_id)
                return view(data, review_id)
        return "Unauthorized", 403



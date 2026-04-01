from flask import Blueprint, request, jsonify
from db import get_db
from auth_middleware import admin_required
from bson import ObjectId
import datetime

reviews_bp = Blueprint('reviews', __name__)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    if 'created_at' in doc:
        doc['created_at'] = str(doc['created_at'])
    return doc

@reviews_bp.route('/reviews', methods=['GET'])
def get_reviews():
    db = get_db()
    reviews = list(db.reviews.find({'approved': True}).sort('created_at', -1))
    return jsonify([serialize(r) for r in reviews])

@reviews_bp.route('/reviews/all', methods=['GET'])
@admin_required
def get_all_reviews():
    db = get_db()
    reviews = list(db.reviews.find().sort('created_at', -1))
    return jsonify([serialize(r) for r in reviews])

@reviews_bp.route('/reviews', methods=['POST'])
def create_review():
    db = get_db()
    data = request.json
    review = {
        'name': data.get('name'),
        'rating': int(data.get('rating', 5)),
        'comment': data.get('comment'),
        'service': data.get('service', 'General'),
        'approved': False,
        'created_at': datetime.datetime.utcnow()
    }
    result = db.reviews.insert_one(review)
    return jsonify({'message': 'Review submitted for approval', 'id': str(result.inserted_id)}), 201

@reviews_bp.route('/reviews/<review_id>/approve', methods=['PATCH'])
@admin_required
def approve_review(review_id):
    db = get_db()
    db.reviews.update_one({'_id': ObjectId(review_id)}, {'$set': {'approved': True}})
    return jsonify({'message': 'Review approved'})

@reviews_bp.route('/reviews/<review_id>', methods=['DELETE'])
@admin_required
def delete_review(review_id):
    db = get_db()
    db.reviews.delete_one({'_id': ObjectId(review_id)})
    return jsonify({'message': 'Review deleted'})

@reviews_bp.route('/reviews/stats', methods=['GET'])
def review_stats():
    db = get_db()
    reviews = list(db.reviews.find({'approved': True}))
    if not reviews:
        return jsonify({'average': 0, 'total': 0, 'distribution': {}})
    total = len(reviews)
    avg = sum(r['rating'] for r in reviews) / total
    dist = {}
    for i in range(1, 6):
        dist[str(i)] = sum(1 for r in reviews if r['rating'] == i)
    return jsonify({'average': round(avg, 1), 'total': total, 'distribution': dist})

from flask import Blueprint, request, jsonify
from db import get_db
from auth_middleware import admin_required
from bson import ObjectId
import datetime

leads_bp = Blueprint('leads', __name__)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@leads_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    db = get_db()
    lead = {
        'name': data.get('name'),
        'phone': data.get('phone'),
        'email': data.get('email', ''),
        'message': data.get('message'),
        'service': data.get('service', 'General'),
        'status': 'new',
        'created_at': datetime.datetime.utcnow()
    }
    result = db.leads.insert_one(lead)
    lead['_id'] = str(result.inserted_id)
    return jsonify({'message': 'Lead submitted successfully', 'id': str(result.inserted_id)}), 201

@leads_bp.route('/leads', methods=['GET'])
@admin_required
def get_leads():
    db = get_db()
    leads = list(db.leads.find().sort('created_at', -1))
    return jsonify([serialize(l) for l in leads])

@leads_bp.route('/leads/<lead_id>', methods=['DELETE'])
@admin_required
def delete_lead(lead_id):
    db = get_db()
    db.leads.delete_one({'_id': ObjectId(lead_id)})
    return jsonify({'message': 'Lead deleted'})

@leads_bp.route('/leads/<lead_id>/status', methods=['PATCH'])
@admin_required
def update_lead_status(lead_id):
    data = request.json
    db = get_db()
    db.leads.update_one({'_id': ObjectId(lead_id)}, {'$set': {'status': data.get('status')}})
    return jsonify({'message': 'Status updated'})

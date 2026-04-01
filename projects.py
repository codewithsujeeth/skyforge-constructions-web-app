from flask import Blueprint, request, jsonify
from db import get_db
from auth_middleware import admin_required
from bson import ObjectId
import datetime, base64

projects_bp = Blueprint('projects', __name__)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    if 'created_at' in doc:
        doc['created_at'] = str(doc['created_at'])
    return doc

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    db = get_db()
    category = request.args.get('category')
    status = request.args.get('status')
    query = {}
    if category and category != 'all':
        query['category'] = category
    if status and status != 'all':
        query['status'] = status
    projects = list(db.projects.find(query).sort('created_at', -1))
    return jsonify([serialize(p) for p in projects])

@projects_bp.route('/projects', methods=['POST'])
@admin_required
def create_project():
    db = get_db()
    data = request.json
    project = {
        'title': data.get('title'),
        'description': data.get('description'),
        'category': data.get('category', 'Construction'),
        'status': data.get('status', 'pending'),
        'location': data.get('location', ''),
        'area': data.get('area', ''),
        'cost': data.get('cost', ''),
        'client': data.get('client', ''),
        'image': data.get('image', ''),
        'images': data.get('images', []),
        'year': data.get('year', str(datetime.datetime.now().year)),
        'created_at': datetime.datetime.utcnow()
    }
    result = db.projects.insert_one(project)
    project['_id'] = str(result.inserted_id)
    return jsonify(project), 201

@projects_bp.route('/projects/<project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
    db = get_db()
    data = request.json
    allowed = ['title', 'description', 'category', 'status', 'location', 'area', 'cost', 'client', 'image', 'images', 'year']
    update = {k: data[k] for k in allowed if k in data}
    db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': update})
    return jsonify({'message': 'Project updated'})

@projects_bp.route('/projects/<project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
    db = get_db()
    db.projects.delete_one({'_id': ObjectId(project_id)})
    return jsonify({'message': 'Project deleted'})

@projects_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    db = get_db()
    project = db.projects.find_one({'_id': ObjectId(project_id)})
    if not project:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(serialize(project))

from flask import Blueprint, request, jsonify
from db import get_db
from auth_middleware import admin_required
import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    db = get_db()
    total_leads = db.leads.count_documents({})
    total_projects = db.projects.count_documents({})
    total_reviews = db.reviews.count_documents({'approved': True})
    pending_projects = db.projects.count_documents({'status': 'pending'})
    approved_projects = db.projects.count_documents({'status': 'approved'})
    done_projects = db.projects.count_documents({'status': 'done'})

    # Monthly leads for last 6 months
    monthly = []
    now = datetime.datetime.utcnow()
    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - datetime.timedelta(days=i*30)).replace(day=1)
        if i > 0:
            month_end = (now.replace(day=1) - datetime.timedelta(days=(i-1)*30)).replace(day=1)
        else:
            month_end = now
        count = db.leads.count_documents({'created_at': {'$gte': month_start, '$lt': month_end}})
        monthly.append({'month': month_start.strftime('%b %Y'), 'count': count})

    # Estimated revenue
    avg_project_value = 500000
    est_revenue = done_projects * avg_project_value

    return jsonify({
        'total_leads': total_leads,
        'total_projects': total_projects,
        'total_reviews': total_reviews,
        'project_status': {
            'pending': pending_projects,
            'approved': approved_projects,
            'done': done_projects
        },
        'monthly_leads': monthly,
        'estimated_revenue': est_revenue,
        'new_leads': db.leads.count_documents({'status': 'new'})
    })

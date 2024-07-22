from flask_restx import fields
from app.extensions import api


ongoing_activities=api.namespace('Ongoing Activities', description='მიმდინარე აქტივობები',path = '/api')
#activities_model = ongoing_activities.model('Activities', {})





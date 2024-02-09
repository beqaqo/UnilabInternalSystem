import os
import uuid

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from werkzeug.utils import secure_filename

from app.models import Project, ProjectUser


class ProjectApi(Resource):

    @jwt_required()
    def post(self):
        name = request.form.get("name")
        description = request.form.get("description")
        url = request.form.get("url")
    
        if "images" in request.files:
            image_files = request.files.getlist("images")

            project = Project(
                name=name,
                description=description,
                url=url
            )   
            project.create()
            project.save()
            
            project_user = ProjectUser(
                user_id=current_user.id,
                project_id=project.id
            )
            project_user.create()
            project_user.save()
        
            base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            images_directory = os.path.join(base_dir, "images", str(project.id))
            os.makedirs(images_directory, exist_ok=True)  

            for image in image_files:
                if image:
                    file_name = str(uuid.uuid4()) + secure_filename(image.filename)
                    image_path = os.path.join(images_directory, file_name)
                    image.save(image_path)

            return "Project was created successfully", 200
    
        return "Failed to create a project or Images weren't sent",  400
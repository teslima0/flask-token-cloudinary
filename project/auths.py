from flask import request,Blueprint,jsonify,make_response
from .models import User,UserSchema,user_schema
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from .import db,app
import bcrypt
import cloudinary
auths=Blueprint('auths',__name__)

@auths.route('/upload_image', methods=['POST'])
#@jwt_required()
def add_prods():
    #current_user_id = get_jwt_identity()
   # data = request.get_json()
    #user = User.query.filter_by(id=current_user_id['username']).first()

    #upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']            
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, folder="image")
            image = app.logger.info(upload_result)
            print(image)
    return {'message': 'Product added successfully'}

@auths.route("/upload", methods=["POST"])
def upload_image():

    file = request.files['file']
    result = cloudinary.uploader.upload(file, folder="image")
    return {"url": result["secure_url"]}

@auths.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user_schema = UserSchema()
    user_data = request.get_json()
    username=user_data['username']
    email=user_data['email']
    password=user_data['password']
  
   
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    errors = user_schema.validate(user_data)

    if errors:
        return {"message": "Validation errors", "errors": errors}, 400
    new_user = User(username=username, email=email, password=hashed_password)    
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

#login route
@auths.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    user_serializer=UserSchema()
    result=user_serializer.dump(user)
    if not user:
        return make_response(jsonify('User Not Found!'), 404)
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=result)  
        return make_response(jsonify(access_token=access_token))
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import cloudinary
from . import db,app
from .models import Product,User
import cloudinary
import cloudinary.uploader
import cloudinary.api

views=Blueprint('views',__name__)
@views.route('/products', methods=['POST'])
#@jwt_required()
def add_product():
    #current_user_id = get_jwt_identity()
    data = request.json()
    #user = User.query.filter_by(id=current_user_id['username']).first()
   
    name=data['name']
    description=data['description']
    price=data['price']
    qty=data['qty']
    
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['image_url']            
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, folder='image')
            image = app.logger.info(upload_result)
            print(image)
    image_url = None
    if data.get('image_url'):
        image_url = cloudinary.uploader.upload(data['image_url'])['secure_url']
        image_url=image_url['secure_url']
    new_product = Product(name, description, price, qty,image_url)

    db.session.add(new_product)
    db.session.commit()

    return {'message': 'Product added successfully'}



def upload_image():

    file = request.files['file']
    result = cloudinary.uploader.upload(file, folder="image")
    return {"url": result["secure_url"]}


@views.route("/Create_products", methods=["POST"])
@jwt_required()
def create_product():
   
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id["id"]).first()
    name = request.form.get("name")
    description = request.form.get("description")
    qty = request.form.get("qty")
    price = request.form.get("price")
    #image = request.files.get("image_url")

    file = request.files['image_url']
    result = cloudinary.uploader.upload(file, folder="image")
    image_url = result["secure_url"]
    #result1=result["secure_url"]
    print(image_url)
    """
    # Upload the image to Cloudinary
    if image:
        result = cloudinary.uploader.upload(image, folder="image")
        image_url = result["secure_url"]
    else:
        return "Image is required", 400
    """
    # Create a product instance and save it to the database
    try:
        product = Product(name=name, description=description, qty=qty, price=price, image_url=image_url, user=user)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        print("Error:", e)

    
    print("Product:", product.__dict__)
    return "Product created successfully", 201
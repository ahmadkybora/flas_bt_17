from flask import Blueprint
from app.Controllers.Panel.UserController import index, store, show, update, delete

userRoute = Blueprint("userRoute", __name__)

userRoute.route('/', methods=['GET'])(index)
userRoute.route('/create', methods=['POST'])(store)
userRoute.route('/<int:user_id>', methods=['GET'])(show)
userRoute.route('/<int:user_id>/edit', methods=['POST'])(update)
userRoute.route('/<int:user_id>', methods=['DELETE'])(delete)
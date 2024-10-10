from flask import Blueprint
from app.routes.homepage import homepage_blueprint
from app.routes.blog_routes import blog_blueprint
from app.routes.user_routes import user_blueprint
from app.routes.category_routes import category_blueprint
from app.routes.course_routes import course_blueprint
from app.routes.event_routes import event_blueprint
from app.routes.training_centers_routes import training_centers_blueprint


main = Blueprint('main', __name__)

main.register_blueprint(homepage_blueprint, url_prefix='/')
main.register_blueprint(blog_blueprint, url_prefix='/')
main.register_blueprint(user_blueprint, url_prefix='/')
main.register_blueprint(category_blueprint, url_prefix='/')
main.register_blueprint(course_blueprint, url_prefix='/')
main.register_blueprint(event_blueprint, url_prefix='/')
main.register_blueprint(training_centers_blueprint, url_prefix='/')
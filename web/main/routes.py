from flask import render_template, request, Blueprint
from web.models import Post
from web.users.utils import top_contributions

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(
        "home.html", posts=posts, top_contributions=top_contributions()
    )

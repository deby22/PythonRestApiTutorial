from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes}"


db.create_all()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the video is required", required=True
)


video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type=str, help="Name of the video is required")
video_patch_args.add_argument("views", type=int, help="Views of the video is required")
video_patch_args.add_argument("likes", type=int, help="Likes of the video is required")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "likes": fields.Integer,
    "videos": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.get_or_404(video_id)
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(404, "blablabla")
        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()
        video = VideoModel.query.get_or_404(video_id)

        if args.get("name"):
            video.name = args["name"]
        if args.get("likes"):
            video.name = args["likes"]
        if args.get("views"):
            video.name = args["views"]
        db.session.commit()
        return video, 201


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)

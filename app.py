#!/usr/bin/env python3
import os
from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_bootstrap import Bootstrap5
from extractor import Extractor
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, "uploads")

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

extractor = Extractor()


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[FileAllowed(photos, "Image only!"), FileRequired("File was empty!")]
    )
    submit = SubmitField("Upload")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        img_loc = f"uploads/{filename}"
        colour_palette = extractor.extract_colour(img_loc, 700, 11, 3)
        file_url = photos.url(filename)
        return render_template("index.html", form=form, file_url=file_url, palette=colour_palette)

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

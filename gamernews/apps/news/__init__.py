from vendor.django_comments.models import Comment
from news.forms import SimpleCommentForm

def get_model():
    return Comment

def get_form():
    return SimpleCommentForm

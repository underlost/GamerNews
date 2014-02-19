from gamernews.vendor.django_comments.models import Comment
from gamernews.apps.news.forms import SimpleCommentForm

def get_model():
    return Comment

def get_form():
    return SimpleCommentForm
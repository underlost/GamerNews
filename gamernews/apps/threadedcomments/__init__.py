from .models import ThreadedComment
from .forms import ThreadedCommentForm

def get_model():
    return ThreadedComment

def get_form():
    return ThreadedCommentForm

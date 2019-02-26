from annoying.decorators import ajax_request, render_to
from blogs.views import blog_list
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from snipts.utils import get_lexers_list
from taggit.models import Tag


@render_to('homepage.html')
def homepage(request):

    if request.blog_user:
        return blog_list(request)

    return {}


@ajax_request
def lexers(request):
    lexers = get_lexers_list()
    objects = []

    for l in lexers:

        try:
            filters = l[2]
        except IndexError:
            filters = []

        try:
            mimetypes = l[3]
        except IndexError:
            mimetypes = []

        objects.append({
            'name': l[0],
            'lexers': l[1],
            'filters': filters,
            'mimetypes': mimetypes
        })

    return {'objects': objects}


def login_redirect(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/' + request.user.username + '/')
    else:
        return HttpResponseRedirect('/')


@render_to('tags.html')
def tags(request):

    all_tags = Tag.objects.filter(snipt__public=True).order_by('name')
    all_tags = all_tags.annotate(count=Count('taggit_taggeditem_items__id'))

    popular_tags = Tag.objects.filter(snipt__public=True)
    popular_tags = popular_tags.annotate(
        count=Count('taggit_taggeditem_items__id'))
    popular_tags = popular_tags.order_by('-count')[:20]
    popular_tags = sorted(popular_tags, key=lambda tag: tag.name)

    return {
        'all_tags': all_tags,
        'tags': popular_tags
    }


@ajax_request
def user_api_key(request):

    if not request.user.is_authenticated():
        return HttpResponseBadRequest()

    return {
        'api_key': request.user.api_key.key
    }

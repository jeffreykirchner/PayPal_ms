'''
root path
'''
from django.http import HttpResponseNotFound

def root_path(request):
    '''
    return page not found for root path
    '''
    return HttpResponseNotFound('<h1>Page not found</h1>')

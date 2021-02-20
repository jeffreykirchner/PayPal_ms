'''
root path
'''
from django.http import HttpResponse

def root_path(request):
    '''
    return page not found for root path
    '''
    return HttpResponse('<h1>Page not found</h1>')

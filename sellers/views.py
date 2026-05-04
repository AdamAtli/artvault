from django.http import HttpResponse

def index(request):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return HttpResponse(f"Responce from {request.path}")

def get_seller_by_id(request, id):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return HttpResponse(f"Responce from {request.path} with id {id}")

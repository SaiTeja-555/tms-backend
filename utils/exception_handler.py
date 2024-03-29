from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError':_handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error 
    }
    
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if response is not None:
        response.data["status_code"] = response.status_code

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_authentication_error(exc, context, response):

    response.data = {
        'error': "Please login to procceed",
        "status_code": response.status_code
    }
    return response

def _handle_generic_error(exc, context, response):
    return response
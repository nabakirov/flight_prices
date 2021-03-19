from functools import wraps
from sanic.exceptions import InvalidUsage


def query_param(request, *query_params, required=False, **kwargs):
    def query_param_decorator(f):
        @wraps(f)
        def function_wrapper(*args, **kwargs):
            params = {}
            for param_key in query_params:
                if request.args.get(param_key) is None and required:
                    raise InvalidUsage(message=f'{param_key} query param required', status_code=400)
                params[param_key] = request.args.get(param_key)
            kwargs = {**kwargs, **params}
            result = await f(*args, **kwargs)
            return result
        return function_wrapper
    return query_param_decorator
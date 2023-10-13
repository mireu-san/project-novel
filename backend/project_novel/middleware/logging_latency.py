import logging
import time

logger = logging.getLogger('middleware')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info('Triggered LoggingMiddleware in logging_latency.py')
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f'Request to {request.path} took {duration:.2f} seconds.') # display in console only.
        logger.info(f'Request to {request.path} took {duration:.2f} seconds.')
        return response


import logging
import time as pytime

from django.db import connection, reset_queries


class SQLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()

        start_time = pytime.time()

        response = self.get_response(request)

        total_time = pytime.time() - start_time

        total_queries = len(connection.queries)

        logging.info(f'Total queries: {total_queries}')
        logging.info(f'Total time: {total_time:.2f} seconds')

        for query in connection.queries:
            sql = query['sql']
            query_time = query['time']  # renamed to query_time
            logging.info(f'Time: {query_time} | Query: {sql}')

        return response

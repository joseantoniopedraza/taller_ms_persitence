
import os

host = os.getenv('REDIS_HOST', 'localhost')
port = int(os.getenv('REDIS_PORT', '6379'))

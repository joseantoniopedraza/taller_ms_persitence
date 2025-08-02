import redis
from redis.exceptions import ConnectionError, TimeoutError
import logging
import sys
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('persistance_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RedisConnect:
    def __init__(self, host, port):
        self.host           = host
        self.port           = port
        self.running        = True 
        self.retry_delay    = 5

    def _connect(self):
        self.r          = redis.Redis(host = self.host, port = self.port)
        self.pubsub     = self.r.pubsub()

    def send(self, message, channel):
        try:
            self._connect()
            logger.info("Sending message to Redis")
            self.r.publish(channel, message)
            logger.info("Message sent successfully")
        except redis.RedisError as e:
            logger.error(f"Failed to send message to Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while sending message: {e}")
            raise

    def _listener(self, channel, callback):
        while self.running:
            try:
                self._connect()
                self.pubsub.subscribe(channel)
                logger.info(f"Listening to channel {channel}...")

                for mensaje in self.pubsub.listen():
                    if not self.running:
                        break
                    if mensaje['type'] == 'message':
                        callback(mensaje['data'])

            except (ConnectionError, TimeoutError) as e:
                logger.warning(f"Redis connection lost: {e}. Reconnecting in {self.retry_delay}s...")
                time.sleep(self.retry_delay)
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Retrying in {self.retry_delay}s...")
                time.sleep(self.retry_delay)
            finally:
                try:
                    if self.pubsub:
                        self.pubsub.unsubscribe(channel)
                        self.pubsub.close()
                except Exception:
                    pass
                try:
                    if self.r:
                        self.r.close()
                except Exception:
                    pass

    def listen(self, channel, callback):
        thread = threading.Thread(target=self._listener, args=(channel, callback), daemon = True)
        thread.start()
        return thread
    
    def stop(self):
        self.running = False


import redis


redis_connection = redis.Redis(host="localhost", port=6379, decode_responses=True)

# redis_connection.set("evyats", 28)
print(redis_connection.get("evyats"))


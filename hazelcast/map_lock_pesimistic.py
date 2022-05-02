import hazelcast
from utility import Value
import time


client = hazelcast.HazelcastClient()
m = client.get_map("map-lock")
key = "1"

m.put_if_absent(key, Value()).result()

print("STARTING")
for i in range(1000):
    if i % 100 == 0:
        print(f"At: {i}")
    m.lock(key).result()
    try:
        value = m.get(key).result()
        time.sleep(0.01)
        value.amount += 1
        m.put(key, value).result()
    finally:
        m.unlock(key).result()

print(f"FINISHED! Result: {m.get(key).result().amount}")

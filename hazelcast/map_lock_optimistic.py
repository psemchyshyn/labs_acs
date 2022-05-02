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
    while True:
        oldValue = m.get(key).result()
        newValue = Value(oldValue)
        time.sleep(0.01)
        newValue.amount += 1
        if m.replace_if_same(key, oldValue, newValue).result():
            break

print(f"FINISHED! Result: {m.get(key).result().amount}")

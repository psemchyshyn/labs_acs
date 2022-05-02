import hazelcast

client = hazelcast.HazelcastClient()
q = client.get_queue("q")

while True:
    v = q.poll().result()
    if v is None:
        continue
    print(f"Consumer got {v}")
import hazelcast

client = hazelcast.HazelcastClient()
q = client.get_queue("q")

for i in range(5):
    print(f"Put {i}")
    q.put(i)

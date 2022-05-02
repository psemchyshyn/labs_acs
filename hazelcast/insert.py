import hazelcast

# Connect to Hazelcast cluster.
client = hazelcast.HazelcastClient()

# Get or create the "distributed-map" on the cluster.
distributed_map = client.get_map("distributed-map")

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient()
# Get the Distributed Map from Cluster.
my_map = client.get_map("my-distributed-map").blocking()

# Standard Put and Get
for i in range(1000):
    my_map.put(str(i), f"value{i}")

# Shutdown the cluster
client.shutdown()
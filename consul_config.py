import consul

session = consul.Consul()

session.kv.put("map", "logging-map")
session.kv.put("queue", "messages-queue")

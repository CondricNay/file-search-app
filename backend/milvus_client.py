from pymilvus import connections, MilvusClient

connections.connect("default", host="127.0.0.1", port="19530")
print(connections.has_connection("default"))

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

# client.create_database(
#     db_name="my_database_1"
# )

client.drop_database(
    db_name="my_database_1"
)
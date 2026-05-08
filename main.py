from json_store import JsonStore

store = JsonStore("data.json")

# Create
store.create("user:1", {"name": "홍길동", "age": 30})
store.create("user:2", {"name": "김철수", "age": 25})

# Read
user = store.read("user:1")
print("Read:", user)

# Read All
all_data = store.read_all()
print("Read All:", all_data)

# Update
store.update("user:1", {"name": "홍길동", "age": 31})
print("Updated:", store.read("user:1"))

# Delete
store.delete("user:2")
print("After Delete:", store.read_all())

# exists
print("user:1 exists?", store.exists("user:1"))
print("user:2 exists?", store.exists("user:2"))

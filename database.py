from models import Task, UpdateTask
from bson import ObjectId
import motor.motor_asyncio

uri = "mongodb+srv://osegutierrez1607:<password>@franklin.ic65u.mongodb.net/?retryWrites=true&w=majority&appName=Franklin"

# Create a new client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(uri)

try:
    client.admin.command('ping')
    print("Conectado a MongoDB!")
except Exception as e:
    print(f"Error al conectar: {e}")

# Send a ping to confirm a
    
db = client["taskdatabase"]
collection = db["tasks"]



async def get_one_task_id(id):
    task = await collection.find_one({"_id": ObjectId(id)})
    return task


async def get_one_task(title):
    task = await collection.find_one({"title": title})
    return task


async def get_all_tasks():
    tasks = []
    cursor = collection.find({})
    async for document in cursor:
        tasks.append(Task(**document))
    return tasks


async def create_task(task: Task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({"_id": new_task.inserted_id})
    return created_task


async def update_task(id: str, data: UpdateTask):
    task = {k: v for k, v in data.dict().items() if v is not None}
    await collection.update_one({"_id": ObjectId(id)}, {"$set": task})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document


async def delete_task(id):
    await collection.delete_one({"_id": ObjectId(id)})
    return True

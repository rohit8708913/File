

import motor, asyncio
import logging 
import motor.motor_asyncio
from config import DB_URI, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

logging.basicConfig(level=logging.INFO)

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return

# **Update Free Usage Count**
async def update_free_usage(user_id):
    try:
        # Check if user exists in DB
        data = await user_data.find_one({"user_id": user_id})

        if not data:
            # If user doesn't exist, create new entry with count = 1
            await user_data.insert_one({"user_id": user_id, "count": 1, "last_reset": time.time()})
        else:
            # Increment count properly
            await user_data.update_one({"user_id": user_id}, {"$inc": {"count": 1}})
    except Exception as e:
        logging.error(f"Error incrementing free usage for user {user_id}: {e}")

    # **Reset Free Usage After 24 Hours**
async def reset_free_usage(user_id):
    try:
        data = await user_data.find_one({"user_id": user_id})
        if data and (time.time() - data.get("last_reset", 0) > 86400):
            await user_data.update_one(
                {"user_id": user_id}, {"$set": {"count": 0, "last_reset": time.time()}}
                )
    except Exception as e:
        logging.error(f"Error resetting free usage for user {user_id}: {e}")

async def check_free_usage(user_id):
    try:
        # Fetch user data from the database
        data = await user_data.find_one({"user_id": user_id})

        if not data:
            return 0  # If no data exists, assume count is 0 (new user)

        # Ensure the count is properly retrieved
        usage_count = int(data.get("count", 0))  # Default to 0 if missing
        return usage_count  # Return actual usage count
    except Exception as e:
        logging.error(f"Error checking free usage for user {user_id}: {e}")
        return 0  # Default to 0 if an error occurs
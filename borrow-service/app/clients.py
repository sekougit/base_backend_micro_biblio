import os
import httpx

BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:8001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8002")


async def get_book(book_id: int):
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{BOOK_SERVICE_URL}/books/{book_id}")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()


async def get_user(user_id: int):
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
# Polling-bot
A simple polling bot to check for available time slots on the termin.bremen.de website for registering apartments 


# To open local dev shell

`make shell`

# How to use User repository

Make sure you have google credentials file in the root of the project named `google.json`.

```python
from core.repository.firebase import UserRepository, UserFirebaseRepository
from core.config import settings

repo: UserRepository = UserFirebaseRepository(credentials=settings.firebase.credentials)
repo.create_user(1001)
repo.create_user(1002)
repo.create_user(1002)
for user_id in repo.get_list_of_users():
    print("user_id = "user_id)
repo.drop_collection()
```

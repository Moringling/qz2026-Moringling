from dataclasses import dataclass, asdict
import json

class UserManager:
    @dataclass
    class User:
        id: int
        name: str
        age: int

        @staticmethod
        def from_dict(d) -> "UserManager.User":
            return UserManager.User(d["id"], d["name"], d["age"])

    def __init__(self) -> None:    
        self.users : dict[int, UserManager.User] = {}
        self.last_id : int = 0

    def _users_dict(self) -> dict[int, dict]:
        return { id: asdict(user) for id, user in self.users.items() }

    def add_user(self, name: str, age: int) -> dict:
        # 题目要求返回字典，问题是字典到底是这个时间的快照，还是一个持久的视图？
        # 如果是前者，那么之后通过 update_age 进行的修改，在返回的字典中不可见
        # 但如果是后者，则意味着调用者可以随意修改用户信息，那就完全破坏了 UserManager 的封装性
        # 综合考虑选择前者，此方法返回的 dict 仅代表此时间的快照，用户修改 dict 中的数据，不会影响 UserManager，同理通过 update_age 修改年龄，也需要重新 get_user 才能看到。
        self.last_id += 1
        new_user = UserManager.User(self.last_id, name, age)
        self.users[self.last_id] = new_user
        return asdict(new_user)


    def get_user(self, id: int) -> dict | None:
        user = self.users.get(id, None)
        if user is None:
            return None
        return asdict(user)

    def update_age(self, id: int, age: int) -> bool:
        user = self.users.get(id, None)
        if user is None:
            return False
        user.age = age
        return True

    def remove_user(self, id: int) -> bool:
        return self.users.pop(id, None) is not None

    def list_users(self) -> list:
        return list(self._users_dict().values())

    def save_to_json(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            obj = {
                "last_id": self.last_id,
                "users": self.list_users()
            }
            json.dump(obj, f, ensure_ascii=False)
    
    def load_from_json(self, path: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                obj = json.load(f)
                if "last_id" not in obj or "users" not in obj or not isinstance(obj["users"], list):
                    return
        except:
            return
        self.users = { int(user["id"]) : UserManager.User.from_dict(user) for user in obj["users"] }
        self.last_id = obj["last_id"]

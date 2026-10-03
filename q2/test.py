import os
import tempfile

from main import UserManager

def tmp_path() -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    return path

def test_add_get():
    man = UserManager()
    assert man.add_user("Alice", 18) == {"id": 1, "name": "Alice", "age": 18 }
    assert man.add_user("Bob", 42) == {"id": 2, "name": "Bob", "age": 42 }
    assert man.get_user(1) == {"id": 1, "name": "Alice", "age": 18 }
    assert man.get_user(2) == {"id": 2, "name": "Bob", "age": 42 }

def test_get_nonexistent_user():
    man = UserManager()
    man.add_user("Alice", 18)
    assert man.get_user(18) is None

def test_update_age():
    man = UserManager()
    id = man.add_user("Alice", 18)["id"]
    assert man.update_age(id, 42)
    assert man.get_user(id) == {"id": 1, "name": "Alice", "age": 42 }

def test_remove_user():
    man = UserManager()
    cindy = man.add_user("Cindy", 42)
    assert man.remove_user(cindy["id"]) is True
    assert man.remove_user(cindy["id"]) is False

def test_list_user_preserve_order():
    man = UserManager()
    man.add_user("Alice", 18)
    man.add_user("Bob", 42)
    assert man.list_users() == [
        {"id": 1, "name": "Alice", "age": 18 },
        {"id": 2, "name": "Bob", "age": 42 }
    ]

def test_json():
    man = UserManager()
    man.add_user("Alice", 18)
    assert man.get_user(1)["name"] == "Alice"
    man.save_to_json("test.json")

    alt = UserManager()
    alt.load_from_json("test.json")
    os.remove("test.json")
    alt.add_user("Bob", 42)
    assert alt.get_user(1)["age"] == 18
    assert alt.get_user(2)["name"] == "Bob"

if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for test in tests:
        try:
            test[1]()
            passed += 1
            print(f"Test {test[0]} PASSED")
        except:
            print(f"Test {test[0]} FAILED")
    if (passed == len(tests)):
        print("All tests passed!")
    else:
        print(f"{passed}/{len(tests)} tests passed.")
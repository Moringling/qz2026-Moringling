import os
import tempfile

from main import analyze_log

def create_temp_jsonl(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, 'w', encoding="utf-8") as f:
        f.write(content)
    return path

def test_normal_file():
    content = """
        {"timestamp": "2026-10-01 10:23:45", "level": "INFO", "message": "用户登录成功", "user": "张三"}
        {"timestamp": "2026-10-01 10:24:01", "level": "ERROR", "message": "数据库连接失败", "user": "李四"}
        {"timestamp": "2026-10-01 10:25:12", "level": "INFO", "message": "用户登出", "user": "张三"}
        {"timestamp": "2026-10-01 10:26:30", "level": "ERROR", "message": "超时", "user": "李四"}
        {"timestamp": "2026-10-01 10:27:00", "level": "INFO", "message": "任务完成", "user": "王五"}
        """

    path = create_temp_jsonl(content)
    try:
        result = analyze_log(path)
        assert result == {
            "total": 5,
            "by_level": { "INFO": 3, "ERROR": 2 },
            "by_user": { "张三": 2, "李四": 2, "王五": 1},
            "last_error": "超时"
        }
    finally:
        os.remove(path)

def assert_empty_result(result : dict):
    assert result == {
        "total": 0,
        "by_level": {},
        "by_user": {},
        "last_error": None
    }

def test_nonexistent_file():
    result = analyze_log("nonexistent_file_123456.jsonl")
    assert_empty_result(result)

def test_empty_file():
    path = create_temp_jsonl("   ")
    try:
        assert_empty_result(analyze_log(path))
    finally:
        os.remove(path)

def test_malformed_json():
    content = """
        {"timestamp": "2026-10-01 10:23:45", "level": "INFO", "message": "用户登录成功", "user": "张三"}
        "timestamp": "2026-10-01 10:24:01", "level": "ERROR", "message": "数据库连接失败", "user": "李四"
        {"timestamp": "2026-10-01 10:25:12", "level": "INFO", "message": "用户登出", "user": "张三"}
        {"timestamp"="2026-10-01 10:26:30", "level"="ERROR", "message"="超时", "user"="李四"}
        {"timestamp": "2026-10-01 10:27:00", "level": "INFO", "message": "任务完成", "user": "王五"}
        """
    path = create_temp_jsonl(content)
    try:
        result = analyze_log(path)
        assert result == {
            "total": 3,
            "by_level": {"INFO": 3},
            "by_user": {"张三": 2, "王五": 1},
            "last_error": None
        }
    finally:
        os.remove(path)

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
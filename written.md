# 选择题 + 简答题

> 本文件包含所有选择题与简答题，请在你的仓库中于本文件作答。
> **硬性要求：本文件所有题目均必须完成，未完成的题目不进入部门筛选流程。**

## 一、选择题（每题 2 分，共 10 题，满分 20 分）

> 说明：单选，将答案写在本节末尾的「答案」行中，格式如 `1. A  2. B  3. C ...`。

1. 依次执行以下代码，输出是什么？

   ```python
   def f(x, lst=[]):
       lst.append(x)
       return lst

   a = f(1)
   b = f(2)
   print(b)
   ```

   - A. `[2]`
   - B. `[1, 2]`
   - C. `[1]`
   - D. `TypeError: 'list' object is not callable`

2. 依次执行以下代码，输出是什么？

   ```python
   a = [1, 2, 3]
   b = a
   c = a.copy()
   a.append(4)
   print(b, c)
   ```

   - A. `[1, 2, 3, 4]  [1, 2, 3, 4]`
   - B. `[1, 2, 3, 4]  [1, 2, 3]`
   - C. `[1, 2, 3]  [1, 2, 3, 4]`
   - D. `[1, 2, 3]  [1, 2, 3]`

3. 依次执行以下代码，输出是什么？

   ```python
   try:
       x = 1 / 0
   except ZeroDivisionError:
       print("A")
   else:
       print("B")
   finally:
       print("C")
   ```

   - A. 只输出 `C`
   - B. 输出 `A` 和 `C`
   - C. 输出 `B` 和 `C`
   - D. 输出 `A`、`B` 和 `C`

4. 依次执行以下代码，输出是什么？

   ```python
   s = "  hello  "
   print(len(s))
   print(len(s.strip()))
   ```

   - A. `7  7`
   - B. `7  5`
   - C. `5  5`
   - D. `5  7`

5. 以下代码的执行结果是？

   ```python
   for i in range(5):
       if i == 3:
           break
   else:
       print("done")
   print("end")
   ```

   - A. 输出 `done` 和 `end`
   - B. 只输出 `end`
   - C. 只输出 `done`
   - D. 什么都不输出

6. 依次执行以下代码，输出是什么？

   ```python
   class Animal:
       def __init__(self, name):
           self.name = name

       def speak(self):
           print("...")

   class Dog(Animal):
       def speak(self):
           print(f"{self.name}: woof")

   d = Dog("Rex")
   d.speak()
   ```

   - A. `...`
   - B. `Rex: woof`
   - C. 输出两行：`...` 和 `Rex: woof`
   - D. `AttributeError: 'Dog' object has no attribute '__init__'`

7. 以下代码中，`d` 的值是什么？

   ```python
   d = {"a": 1, "b": 2}
   d = {k: v for k, v in d.items() if v > 1}
   print(d)
   ```

   - A. `{'a': 1, 'b': 2}`
   - B. `{'b': 2}`
   - C. `{1: 'a', 2: 'b'}`
   - D. `SyntaxError: invalid syntax`

8. 依次执行以下代码，输出是什么？

   ```python
   import json
   s = json.dumps({"name": "张三", "age": 18})
   print(type(s))
   ```

   - A. `<class 'dict'>`
   - B. `<class 'str'>`
   - C. `<class 'bytes'>`
   - D. `TypeError: dump() missing 1 required positional argument: 'fp'`

9. 依次执行以下代码，输出是什么？

   ```python
   def f(x):
       return x + 1

   f(5)
   print(f(5))
   ```

   - A. 输出两行：`None` 和 `6`
   - B. 只输出 `6`
   - C. 只输出 `None`
   - D. 输出 `6` 两次

10. 以下代码中，`user.get("city")` 和 `user["city"]` 的区别是什么？

    ```python
    user = {"name": "张三", "age": 18}
    ```

    - A. 没有区别，两者行为完全一致
    - B. `get()` 返回默认值 `None`，`[]` 抛出 `KeyError`
    - C. `get()` 抛出 `KeyError`，`[]` 返回 `None`
    - D. `get()` 只能用于字符串键，`[]` 可以用于任意键

### 答案

（在此填写，格式：`1. A  2. B  3. C  4. D  5. A  6. B  7. C  8. D  9. A  10. B`）

1. B  2. B  3. B  4. B  5. B  6. B  7. B  8. B  9. B  10. B

---

## 二、简答题（每题 10 分，共 3 题，满分 30 分）

> 说明：直接在本文件对应题目下方作答，支持代码块。

### 第 1 题：浅拷贝与深拷贝

以下代码中，`a`、`b`、`c` 三者之间的关系是什么？执行 `a[0].append(99)` 后，`b` 和 `c` 分别变成什么？请解释原因。

```python
a = [[1, 2], [3, 4]]
b = a.copy()
import copy
c = copy.deepcopy(a)
```

b 是 a 的浅拷贝，b、a是不同对象，但是b、a中的元素是相同对象（b[0]和a[0]是同一个列表，b[1]和a[1]是同一个列表）

c 是 a 的深拷贝，c、a是不同对象，并且c、a中的元素也都是不同对象

执行 `a[0].append(99)` 后，由于 a[0] 和 b[0] 是同一个对象，因此b会变成 `[[1, 2, 99], [3, 4]]`。而 c[0] 与 a[0] 不是同一个对象，因此 c 仍为 [[1, 2], [3, 4]]

### 第 2 题：字典与列表的综合应用

以下代码模拟"从日志中提取用户信息"，请回答：

```python
logs = [
    {"user": "张三", "action": "login", "level": "INFO"},
    {"user": "李四", "action": "logout", "level": "INFO"},
    {"user": "张三", "action": "error", "level": "ERROR"},
    {"user": "王五", "action": "login", "level": "INFO"},
    {"user": "李四", "action": "error", "level": "ERROR"},
]
```

1. 写出表达式，找出所有 `level` 为 `"ERROR"` 的日志（返回字典列表）。
2. 写出表达式，统计每个用户出现了几次（返回字典，键为用户名，值为次数）。
3. 解释为什么第 2 问不能直接用 `len(logs)` 得到结果，需要什么遍历结构？

1. errors = [ log for log in logs if log["level"] == "ERROR" ]
2. 
  ```python
  from collections import Counter
  user_to_count = Counter(log["user"] for log in logs)
  user_to_count_dict = dict(user_to_count)
  ```
3. len(logs) 只是返回了 logs 这个字典的长度，即 5。遍历结构如下：
  ```python
  user_to_count = {}
  for log in logs:
    user = log["user"]
    user_to_count[user] = user_to_count.get(user, 0) + 1
  ```

### 第 3 题：异常处理设计

Day_10 中你写过 `safe_int(s)` 函数：能转就返回整数，不能转就返回 `None`。

现在请你设计一个 `safe_divide(a, b)` 函数：

- 输入两个字符串 `a` 和 `b`
- 尝试将它们转为数字并计算 `a / b`
- 如果转换失败（`ValueError`）或除数为零（`ZeroDivisionError`），返回 `None`
- 否则返回商（`float`）

请写出函数代码，并说明：为什么这里用 `try/except` 比先用 `if` 判断再计算更好？

```python
def safe_divide(a : str, b : str) -> float :
    try:
        x = float(a)
        y = float(b)
        return x / y
    except (ValueError, ZeroDivisionError):
        return None
```

为什么这里用 `try/except` 比先用 `if` 判断再计算更好？
首先 if 很难判断字符串能不能转化为 float，而且 try-except 更为简洁，可以同时捕获上述转化错误和除以0的错误。

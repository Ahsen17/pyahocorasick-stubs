[English](README.md) | **简体中文**

# pyahocorasick-stubs

为 Unicode 版 [pyahocorasick](https://github.com/WojciechMula/pyahocorasick) 2.3.1
提供的独立 [PEP 561](https://peps.python.org/pep-0561/) stub-only 类型包。它让
mypy、pyright 等类型检查器精确理解 `ahocorasick` C 扩展 —— `Automaton` 类、
存储与键模式、模块级 `load()`。只含类型，不含任何运行时代码。要求 Python 3.12+。

## 安装

本包直接从 GitHub 分发（尚未发布到 PyPI）：

```bash
pip install git+https://github.com/Ahsen17/pyahocorasick-stubs.git
```

或使用 [uv](https://docs.astral.sh/uv/)：

```bash
uv add git+https://github.com/Ahsen17/pyahocorasick-stubs.git
```

安装本包时会自动带入兼容版本的 `pyahocorasick`（已声明为依赖）。mypy 与 pyright
均无需任何配置即可识别这些 stub。

## 快速上手

```python
from ahocorasick import Automaton

# 泛型下标只是静态记法：注解写 Automaton[str]，
# 构造时始终用不带下标的 Automaton()。
words: Automaton[str] = Automaton()  # 默认存储模式：STORE_ANY（必须提供值）
words.add_word("he", "he")
words.add_word("her", "her")
words.add_word("here", "here")
words.make_automaton()

for end_index, value in words.iter("here"):
    print(end_index, value)  # 1 he / 2 her / 3 here
```

存储与键模式通过位置参数选择：

```python
from ahocorasick import KEY_SEQUENCE, STORE_INTS, STORE_LENGTH, Automaton

integers = Automaton(STORE_INTS)  # Automaton[int, str, Literal[10]]
integers.add_word("x", 42)

lengths = Automaton(STORE_LENGTH)  # 值由键长度推导
lengths.add_word("abc")  # get("abc") == 3

sequence = Automaton(STORE_ANY, KEY_SEQUENCE)  # tuple[int, ...] 键
sequence.add_word((1, 2), "one-two")
```

值得了解的行为，stub 均已静态约束：

- `add_word()` 在 `STORE_ANY` 下必须提供值，在 `STORE_INTS` 下可省略整数值，
  在 `STORE_LENGTH` 下忽略传入的值。
- `iter()` 是唯一接受关键字参数的方法；搜索迭代器支持 `set()` 以实现分块输入。
- 构造函数关键字参数不会改变运行时模式 —— C 扩展在该处仅接受位置参数。

## 版本策略

stub 版本号在其对齐的上游版本之后追加一个 stub 修订号：`2.3.1.0` 对应
`pyahocorasick` 2.3.1；上游未发新版而 stub 有变更时，末位修订号递增。运行时依赖
已固定到兼容的上游版本区间（`pyahocorasick>=2.3.1,<2.4`）；请将本 stub 包与
`pyahocorasick` 同步升级。

## 验证

这些 stub 对照真实的 pyahocorasick C 扩展验证：运行时集成测试覆盖完整的公开
API，mypy 与 pyright 均以 strict 模式对类型层测试套件进行检查。

## 许可证

[MIT](LICENSE)

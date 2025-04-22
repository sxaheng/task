import random
import string
import time


def struct_data_sampling(num, seed=None, **kwargs):
    """
    使用**kwargs定义的结构生成指定数量的随机样本数据。
    支持生成器方式返回样本，适用于超大数据量。
    :param num: 样本数量
    :param seed: 随机种子（可选）
    :param kwargs: 定义数据结构的嵌套字典
    :yield: 单个样本
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())

    def generate(config):
        if isinstance(config, dict):
            if len(config) == 1 and list(config.keys())[0] in ('int', 'float', 'str'):
                return generate_basic_type(config)
            else:
                return {key: generate(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [generate(random.choice(config)) for _ in range(random.randint(1, 5))]
        elif isinstance(config, tuple):
            return tuple(generate(item) for item in config)
        else:
            return config

    def generate_basic_type(config):
        key = list(config.keys())[0]
        settings = config[key]
        if key == 'int':
            return random.randint(*settings.get('datarange', (0, 100)))
        elif key == 'float':
            return random.uniform(*settings.get('datarange', (0.0, 10000.0)))
        elif key == 'str':
            chars = settings.get('datarange', string.ascii_letters)
            length = settings.get('len', 8)
            return ''.join(random.choice(chars) for _ in range(length))
        return None

    for _ in range(num):
        yield generate(kwargs)


def print_values(data, indent=0):
    """
    递归打印样本中的所有值
    """
    prefix = ' ' * indent
    if isinstance(data, (int, float, str)):
        print(prefix + str(data))
    elif isinstance(data, dict):
        for key, value in data.items():
            print(prefix + f"{key}:")
            print_values(value, indent + 2)
    elif isinstance(data, (list, tuple)):
        for i, item in enumerate(data):
            print(prefix + f"[{i}]:")
            print_values(item, indent + 2)


def apply():
    structure = {
        "int": {"int": {"datarange": (0, 100)}},
        "float": {"float": {"datarange": (0, 10000)}},
        "str": {"str": {"datarange": string.ascii_uppercase, "len": 10}},
        "tuple": (
            {"str": {"datarange": string.ascii_lowercase, "len": 5}},
            {"int": {"datarange": (10, 20)}}
        ),
        "list": [
            {"int": {"datarange": (0, 10)}},
            {"str": {"datarange": "ABCDEFG", "len": 3}}
        ],
        "dict": {
            "name": {"str": {"datarange": string.ascii_letters, "len": 8}},
            "age": {"int": {"datarange": (18, 60)}},
            "scores": {
                "math": {"int": {"datarange": (60, 100)}},
                "english": {"int": {"datarange": (60, 100)}}
            }
        }
    }

    samples = struct_data_sampling(100000000, **structure)  # 一亿个样本

    for i, sample in enumerate(samples):
        if i < 5:
            print(f"\n=== Sample {i + 1} ===")
            print_values(sample)
        if i >= 4:  # 只展示前5个
            break


if __name__ == "__main__":
    apply()

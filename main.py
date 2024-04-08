import dataclasses
import inspect
import json
import cantools


def test():
    # 获取调用方
    frame = inspect.currentframe().f_back
    # 获取调用方文件绝对路径
    caller_file = inspect.getfile(frame)
    # 这种方式也可以
    caller_file = frame.f_code.co_filename

    ...

    # 获取调用方函数名
    print(frame)
    print(caller_file)


def hello_1():
    test()


hello_1()


# 新建一个类 注解(装饰器) ,这个注解会给类添加一个静态属性 int,每次创建一个对象,这个属性就会自增1
def auto_increment(cls):
    cls.count = 0
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        cls.count += 1
        self.count = cls.count

    cls.__init__ = new_init

    def print_count(self):
        print(self.count)

    cls.print_count = print_count
    return cls


@auto_increment
class A:
    def __init__(self, name):
        self.name = name


a = A("a")
a.print_count()
b = A("b")
b.print_count()
a.print_count()
print(A.count)


class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


def create_animal(kind, name):
    if kind == "Dog":
        return Dog(name)
    elif kind == "Cat":
        return Cat(name)
    else:
        raise ValueError(f"Unknown animal kind: {kind}")


def make_animal_sound(animal):
    make_sound_method = getattr(animal, "make_sound")
    return make_sound_method()


dog = create_animal("Dog", "Rover")
cat = create_animal("Cat", "Fluffy")

# 让它们发出声音
print(make_animal_sound(dog))  # 输出: Woof!
print(make_animal_sound(cat))  # 输出: Meow!


# 编写一个新的 装饰器,这个装饰器会给类的每个属性添加一个 setter 和 getter 方法 比如 属性name,就会有一个方法 setname 和 getname  这个方法会设置和获取属性的值
def add_properties(cls):
    for name, type_ in cls.__annotations__.items():

        def getter(self, name=name):  # 使用默认参数立即捕获name的值
            return getattr(self, f"{name}")

        def setter(self, value, name=name, type_=type_):  # 使用默认参数立即捕获name和type_的值
            if not isinstance(value, type_):
                raise TypeError(f"Expected type {type_} for {name}, but got type {type(value)}")
            setattr(self, f"{name}", value)

        setattr(cls, f"get{name}", getter)
        setattr(cls, f"set{name}", setter)
    return cls


@add_properties
@dataclasses.dataclass
class Person:
    name: str
    age: int


p = Person("Alice", 30)
p.setname("Tom")
p.setage(20)
print(p.getname())  # 输出: Tom
print(p.getage())  # 输出: 20
print(p)
# print(p.__annotations__)

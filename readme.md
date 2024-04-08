### python 反射学习 

#### 编写一个新的 装饰器,这个装饰器会给类的每个属性添加一个 setter 和 getter 方法 比如 属性name,就会有一个方法 setname 和 getname  这个方法会设置和获取属性的值

```py
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


```

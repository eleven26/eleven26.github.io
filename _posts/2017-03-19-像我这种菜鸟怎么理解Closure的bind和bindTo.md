---
published: true
title: 像我这种菜鸡怎么理解Closure的bind和bindTo
layout: post
category: php
---

bind是bindTo的静态版本，因此只说bind吧。(还不是太了解为什么要弄出两个版本)

> 官方文档: 复制一个闭包，绑定指定的$this对象和类作用域。
其实后半句表述很不清楚。
> 我的理解: 把一个闭包转换为某个类的方法(只是这个方法不需要通过对象调用), 这样闭包中的$this、static、self就转换成了对应的对象或类。

因为有几种情况:
> 1、只绑定$this对象.
> 2、只绑定类作用域.
> 3、同时绑定$this对象和类作用域.(文档的说法)
> 4、都不绑定.(这样一来只是纯粹的复制, 文档说法是使用cloning代替bind或bindTo)

下面详细讲解这几种情况:

#### 1、只绑定$this对象

{% hightlight php %}
$closure = function ($name, $age) {
    $this->name = $name;
    $this->age = $age;
};

class Person {
    public $name;
    public $age;

    public function say() {
        echo "My name is {$this->name}, I'm {$this->age} years old.\n";
    }
}

$person = new Person();

//把$closure中的$this绑定为$person
//这样在$bound_closure中设置name和age的时候实际上是设置$person的name和age
//也就是绑定了指定的$this对象($person)
$bound_closure = Closure::bind($closure, $person);

$bound_closure('php', 100);
$person->say();
{% endhighlight %}

> My name is php, I'm 100 years old.

> 注意: 在上面的这个例子中，是不可以在$closure中使用static的，如果需要使用static，通过第三个参数传入带命名空间的类名。

#### 2、只绑定类作用域.

{% hightlight php %}
$closure = function ($name, $age) {
  static::$name =  $name;
  static::$age = $age;
};

class Person {
    static $name;
    static $age;

    public static function say()
    {
        echo "My name is " . static::$name . ", I'm " . static::$age. " years old.\n";
    }
}

//把$closure中的static绑定为Person类
//这样在$bound_closure中设置name和age的时候实际上是设置Person的name和age
//也就是绑定了指定的static(Person)
$bound_closure = Closure::bind($closure, null, Person::class);

$bound_closure('php', 100);

Person::say();
{% endhighlight %}

> My name is php, I'm 100 years old.

> 注意: 在上面的例子中，是不可以在$closure中使用$this的，因为我们的bind只绑定了类名，也就是static，如果需要使用$this，新建一个对象作为bind的第二个参数传入。

#### 3、同时绑定$this对象和类作用域.(文档的说法)

{% hightlight php %}
$closure = function ($name, $age, $sex) {
    $this->name = $name;
    $this->age = $age;
    static::$sex = $sex;
};

class Person {
    public $name;
    public $age;

    static $sex;

    public function say()
    {
        echo "My name is {$this->name}, I'm {$this->age} years old.\n";
        echo "Sex: " . static::$sex . ".\n";
    }
}

$person = new Person();

//把$closure中的static绑定为Person类, $this绑定为$person对象
$bound_closure = Closure::bind($closure, $person, Person::class);
$bound_closure('php', 100, 'female');

$person->say();
{% endhighlight %}

> My name is php, I'm 100 years old.
> Sex: female.

> 在这个例子中可以在$closure中同时使用$this和static

#### 4、都不绑定.(这样一来只是纯粹的复制, 文档说法是使用cloning代替bind或bindTo)

{% hightlight php %}
$closure = function () {
    echo "bind nothing.\n";
};

//与$bound_closure = clone $closure;的效果一样
$bound_closure = Closure::bind($closure, null);

$bound_closure();
{% endhighlight %}

> bind nothing.

> 这个就用clone好了吧...



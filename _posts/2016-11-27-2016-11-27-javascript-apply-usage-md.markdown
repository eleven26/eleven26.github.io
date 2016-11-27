---
published: true
title: 2016-11-27-javascript-apply-usage.md
layout: post
---
---
published: true
title: javascript apply和call方法详解
layout: post
category: Javascript
---

1. apply和call的区别在哪里
2. apply和call的用法
3. 什么情况下用apply，什么情况下用call
4. apply的其他巧妙用法

##### apply和call的区别
apply和call的主要区别是apply第二个参数为数组，而call用参数列表来代替这个数组。

##### apply和call的用法
[apply方法的定义](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply)
apply()方法使用一个this对象和数组做为参数来调用对应的function，如
{% highlight javascript %}
fun.apply(thisArg, [argsArray])
{% endhighlight %}
返回值: 返回已改变的this和额外参数的函数。
描述: 正常情况下，我们在function里面使用this的时候，this是当前运行环境的相关对象，不同环境下运行可能不一样，在浏览器是Window对象，在命令行用node运行又是另外一个对象。通过apply和call我们可以改变这个this对象，如
{% highlight javascript %}
function Person(name, age){
    this.name = name;
    this.age = age;
    console.log(this);
}
function Student(name, age, grade){
    Person.apply(this, arguments);
    this.grade = grade;
}
var person = new Person("c", "30");
var student = new Student("golang", "5", "一年级");
{% endhight %}
上面的例子中，第一次new Person的时候，this是
{% highlight javascript %}
Person {name: "c", age: "30"}
{% endhighlight %}
第二次this是
{% highlight javascript %}
Student {name: "golang", age: "5"}
{% endhighlight %}
也就是说，第二次Person里面的this虽然还是在Person对象内，但是this值已经改变了，变成了我们传递进去的this对象。
但是，除了this，我们还可以传递其他对象，这个this只是指调用apply那个对象中的this。

利用这个特性，对于一些只接受参数列表的内置函数，我们可以通过apply来传入一个数组参数，thisArg传入null就好：
{% highlight javascript %}
var numbers = [5, 6, 2, 3, 7];
var max = Math.max.apply(null, numbers); 
var min = Math.min.apply(null, numbers);
{% endhighlight %}

##### 什么情况用apply，什么情况用call
在给对象参数的情况下，如果参数是数组，并且和调用apply的函数列表参数顺序一致，则可以采用apply，上面的person和student的例子中，如果person中的参数列表是形如age,name的话，这样我们就不能使用apply了，因为student中的参数顺序是name,age,grade，直接用apply传arguments数组过去的话，就是把name赋值给age了，这种情况我们就需要使用call了，Person.call(age,name,grade)

##### apply的其他巧妙用法
上面的例子中，在调用Person的时候，Person需要的不是数组，但是为什么我们给它一个数组它仍然可以解析为一个一个的参数。
这个就是apply的巧妙之处，可以将一个数组转换了一个参数列表。
另外一个用法，使用push结合apply进行数组合并：
{% highlight javascript %}
var arr1 = [1,2,3];
var arr2 = [4,5,6];
Array.ptototype.push.apply(arr1, arr2);
{% endhighlight %}

---
published: true
title: C++函数指针(译)
layout: post
category: C++
---

　　函数指针是一个存储函数地址以便后续调用的指针变量。这是一个非常有用的功能，因为函数封装了行为。例如，每次你需要一个特定行为如画一条线，你就可以使用函数调用代替写一大堆重复代码。但有时候你想使用本质上相同的代码在不同的调用中选择不同的行为。继续阅读下面的具体例子。

## 使用函数指针的例子

#### 使用函数做其他函数的参数

　　如果你要写一个排序函数，你可能会允许函数调用者选择数据排序的顺序，一部分程序员可能需要有小到大排序，其他人可能需要与此类似的由大到小排序。让你的用户选择哪种方式的一个方法是给函数提供一个标志位作为参数，但这样不方便，因为排序函数有固定的比较类型集合(如顺序和逆序)。

　　让用户选择排序数据方式的一个更好的方法是，让用户传递一个函数给排序函数。这个函数可能需要两个参数来实现两个参数之间的比较。我们将会探讨一些函数指针的语法。

#### 回调函数
　　函数指针的另外一个用法是，设置当某个特定事件发生的时候的调用的"listener"或者"callback"函数。回调函数被调用的时候会执行回调函数内的代码。

　　你为什么会在你的代码中使用回调函数？你在使用其他人写的类库的时候可能经常会看到回调函数。一个例子是当你写图形用户界面(GUI)的时候，大部分时间，用户都是在移动鼠标指针和重新绘制界面的循环中。然而，有些时候，用户按下一个按钮并在表单域输入一串文本，这些操作就是需要你的程序进行一些特定的处理来响应的"事件"。使用回调函数可以让你的代码知道正在发生什么。用户的点击应该导致界面去调用一个函数来处理这个点击事件。

　　为了对此有一个更加具体的了解，想一下当你使用一个有"create_fnction"函数的GUI库的时候会发生什么。那会占用屏幕上按钮本来应该出现的地方，并带有文本和一个点击的时候调用的函数。假定目前C(和C++)有一个通用的带有"函数指针"类型参数的函数，它看起来应该像下面那样。
{% highlight C++ %}
void create_button(int x, int y, const char *text, function callback_func);
{% endhighlight %}

　　无论什么时候按钮被点击，callback_func会被调用。callback_func具体做了什么依赖于那个按钮，这就是create_button函数使用函数指针非常有用的原因。

## 函数指针语法
　　声明函数指针的语法一眼看上去可能有点凌乱，但当你明白明白发生了什么的时候，就会发现其实非常直截了当。让我们看下下面这个简单的例子：
{% highlight C++ %}
void (*foo)(int);
{% endhighlight %}
　　在这个例子中，foo是有一个整形参数，返回值为void类型的函数指针。它看起来像是你声明了一个名字为"*foo"，参数为一个整型参数，返回值为void类型的函数。如果 *foo 是一个函数，那么foo必须指向一个函数。(与此类似，像int *x的声明可以读作*x是一个整数，因此x必须是一个指向整数的指针。)

　　声明函数指针的关键是，使用(*func_name)代替通常情况下的func_name。

#### 阅读函数指针声明
　　当更多*号出现在函数指针声明中的时候人们会感到困惑：
{% highlight C++ %}
void *(*foo)(int *);
{% endhighlight %}
　　在这里，阅读的关键是由内到外，你们应该注意到最内层的表达式元素是*foo，其他部分看起来像是一个正常的函数声明。*foo应该指向一个返回值类型为void *和需要一个int *参数的函数。因此，foo是一个指向这样一个函数的指针。

#### 初始化函数指针
　　为了初始化函数指针，你必须把函数地址赋给函数指针。语法类似其他指针变量：
{% highlight C++ %}
void my_int_func(int x)
{
    printf("%d\n", x);
}
{% endhighlight %}

int main()
{
    void (*foo)(int);
    /* 取地址符实际上是可选的 */
    foo = &my_int_func;

    return 0;
}

#### 使用函数指针
　　为了使用函数指针指向的函数，你可以把函数指针当做你要调用的函数。调用函数指针的行为会自动进行解引用的操作，而不需要手动解引用：
{% highlight C++ %}
void my_int_func(int x)
{
    printf("%d\n", x);
}

int main()
{
    void (*foo)(int);
    foo = &my_int_func;

    /* 调用my_int_func (注意:你不需要写成 (*foo)(2)) */
    foo(2);
    /* 但如果你想这样做也可以 */
    (*foo)(2);

    return 0;
}
{% endhighlight %}
　　函数指针比较灵活，它和大部分指针的用法一致，甚至可以省略部分语法。这类似于数组，空数组会退化为一个指针，但你同样可以使用&获取它的地址。

#### 真实环境的函数指针
　　(Let's go back to the sorting example where I suggested using a function pointer to write a generic sorting routine where the exact order could be specified by the programmer calling the sorting function.)(还没想好怎么翻译),其实C语言的函数qsort就是那样做的。

　　从linux的手册页可以看到以下定义：
{% highlight C++ %}
void qsort(void *base, size_t nmemb, size_t size,
           int(*compar)(const void*, const void*));
{% endhighlight %}

　　void*的使用允许qsort操作任何类型的数据(在C++中，你通常会使用模板来完成这类任务，但是C++通用允许使用void*指针)，因为void*指针能指向任何类型。由于我们不知道void* array中的具体元素数量，我们必须把待排序的数组的元素数量nmemb传给qsort，而不是一般情况下的输入长度、大小。

　　但我们感兴趣的是传递给qsort的参与比较的参数:这是一个带有两个void*类型参数并返回一个int型的函数指针。这允许任何人指定怎么排序这些数组的元素而不用写一个特定的排序算法。同样需要注意的是，比较返回一个int型数字，函数指针指向的函数应该返回-1如果第一个参数小于第二个参数，如果相等返回0，如果第二个参数小于第一个参数则返回1。

　　例如，把一个数组升序排列，我们可以写成下面这样:
{% highlight C++ %}
#include<stdlib.h>

int int_sorter(const void *first_arg, const void *second_arg)
{
    int first = *(int*)first_arg;
    int second = *(int*)second_arg;
    if (first < second){
        return -1;
    }else if(first == second){
        return 0;
    }else if(first > second){
        return 1;
    }
}

int main()
{
    int array[10];
    int i;
    /* fill array*/
    for(i = 0; i < 10; ++i)
    {
        array[i] = 10 - i;
    }
    qsort(array, 10, sizeof(int), int_sorter);
    for(i = 0; i < 10; ++i)
    {
        printf("%d\n", array[i]);
    }
}
{% endhighlight %}


#### 使用多态和虚函数代替函数指针(C++)
　　通过虚函数你通常可以避免使用具体的函数指针。例如，你可以使用含有名字为compare的虚函数的类对象指针代替函数指针。
{% highlight C++ %}
class Sorter
{
    public:
    virtual int compare(const void *first, const void *second);
};

//cpp_qsort, a qsort using C++ features like virtual functions
void cpp_qsort(void *base, size_t nmemb, size_t size, Sorter *compar);
{% endhighlight %}

　　在cpp_qsort内部，无论什么时候需要比较，compar->compare应该被调用。对于那些重写了这个虚函数的类，排序例程将会获得那个虚函数的行为，例如:
{% highlight C++ %}
class AscendSorter : public Sorter
{
    virtual int compare (const void*, const void*)
    {
        int first = *(int*)first_arg;
        int second = *(int*)second_arg;
        if(first < second){
          return -1;
        }else if(first == second){
          return 0;
        }else{
          return 1;
        }
    }
};
{% endhighlight %}
　　然后你就可以传递一个AscendSorter实例的指针给cpp_qsort来对整数进行升序排列。

#### 但是你真的没有使用函数指针吗？
　　虚函数背后是用函数指针实现的，因此你还是在使用函数指针，它仅仅在编译器层面帮你完成了函数指针的工作。使用多态是一个比较合适的策略，但是会带来创建对象的开销，而不是简单地传递一个函数指针。

### 函数指针概括

#### 语法
* 声明
　　声明一个函数指针与声明函数类似，除了函数名使用*foo而不是foo:
{% highlight C++ %}
void (*foo)(int);
{% endhighlight %}

* 初始化
你可以通过函数名来获取函数的地址:
{% highlight C++ %}
void foo();
func_pointer = foo;
{% endhighlight %}
　　或者在函数名前使用取地址符:
{% highlight C++ %}
void foo();
func_pointer = &foo;
{% endhighlight %}

* 调用
调用函数指针指向的函数和调用函数一样:
{% highlight C++ %}
func_pointer(arg1, arg2);
{% endhighlight %}
　　或者你也可以选择在调用函数之前对函数指针进行解引用:
{% highlight C++ %}
(*func_pointer)(arg1, arg2);
{% endhighlight %}

* 使用函数指针的好处:
函数指针提供了一个传递怎样做一件事的指令的方式;
通过允许开发者传递不同的函数指针作为参数，你可以写出灵活的函数和类库;
虚函数同样可以通过虚函数实现。

> 译自: <a href="http://www.cprogramming.com/tutorial/function-pointers.html">http://www.cprogramming.com/tutorial/function-pointers.html</a>

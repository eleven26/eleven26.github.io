---
published: true
title: C++使用函数指针
layout: post
category: C++
---

函数指针是存储函数地址以便后续通过该地址调用函数的指针，下面例子中compare函数可以传入不同的函数指针，根据传入的函数指针，我们可以得到同一个数组按照不同方法排序后的结果。

{% highlight c++ %}
#include<iostream>
#include<cstdlib>
using namespace std;

#ifndef DEBUG
#define DEBUG
#endif

#undef DEBUG

short ascend(int a, int b){
    if (a == b) return 0;
    return a > b ? 1 : -1;
}

short descend(int a, int b){
    if (a == b) return 0;
    return a > b ? -1 : 1;
}

void print_arr(int *array, int len) {
    for(int i=0;i<len;++i){
        cout << array[i] << " ";
    }
    cout << endl;
}

int* compare(int array[], int len, short (*sort_function)(int, int)){
#ifdef DEBUG
    print_arr(array, len);
#endif
    int *temp = (int*)calloc(len, sizeof(int));
    int temp_data;
    for (int i=0; i < len - 1; ++i){
        for (int j=i+1; j < len; ++j){
            if (sort_function(array[i], array[j]) > 0){
                temp_data = array[i];
                array[i] = array[j];
                array[j] = temp_data;
            }
            temp[i] = array[i];
            if (j == len - 1)
                temp[j] = array[j];
    }
}
#ifdef DEBUG
    print_arr(array, len);
#endif
    return temp;
}

int main(){
  int array[5] = {5,2,4,3,1};
  int array_len = sizeof(array) / sizeof(int);
#ifdef DEBUG
  cout << "array_len = " << array_len << endl;
#endif
  cout << "source array : ";
  print_arr(array, array_len);

  int *temp = (int*)calloc(array_len, sizeof(int));
  memcpy(temp, compare(array, array_len, descend), sizeof(int)*array_len);
  cout << "descending order : ";
  print_arr(temp, array_len);
  memcpy(temp, compare(array, array_len, ascend), sizeof(int)*array_len);
  cout << "ascending order : ";
  print_arr(temp, array_len);
  return 0;
}
{% endhighlight %}


输出：
{% highlight output %}
~$ g++ test.cpp
~$ ./a.out
source array : 5 2 4 3 1
descending order : 5 4 3 2 1
ascending order : 1 2 3 4 5
{% endhighlight %}

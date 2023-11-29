# Markdown 规范模板

## 文本样式

- **加粗文本**: **这是加粗的文本**
- *斜体文本*: *这是斜体的文本*
- ~~删除文本~~：~~这是删除的文本~~

## 列表

### 有序列表
1. 第一项
2. 第二项
3. 第三项

### 无序列表
- 项目一
- 项目二
- 项目三

## 字号大小

<font size="1">小号字体</font>  
<font size="3">正常字体</font>  
<font size="5">大号字体</font>

## 字体颜色

<font color="red">红色文本</font>  
<font color="green">绿色文本</font>  
<font color="blue">蓝色文本</font>

## 表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 1   | A   | X   |
| 2   | B   | Y   |
| 3   | C   | Z   |

## 插入图片

![图片描述](地址.jpg)

## 居中

<center>这是一段文字</center> 

## 公式

### 矩阵 
$$
\begin{vmatrix}
\frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} & \ldots & \frac{\partial f_1}{\partial x_n} \\
\frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} & \ldots & \frac{\partial f_2}{\partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_n}{\partial x_1} & \frac{\partial f_n}{\partial x_2} & \ldots & \frac{\partial f_n}{\partial x_n} \\
\end{vmatrix}
$$

### 分段函数
$$
f(x,y)=\begin{cases}
        \frac{1}{A}&(x,y)\in D \\
        0&others
     \end{cases}
$$

### 多行公式
$$
\begin{aligned}
  P(x_2=1)=&\frac{m}{n}\cdot \frac{m-1}{n-1}+\frac{n-m}{n}\cdot \frac{m}{n-1}\\
  &=\frac{m^2-m+nm-m^2}{n(n-1)}\\
  &=\frac{m}{n}
\end{aligned}
$$
***注***：公式中的\\\后面请紧跟换行符\n
否则转化时可能出现\\丢失的情况

## 代码块
```语言
这是一段代码块
```
***注***：在使用md中代码块时要符合两个```之间填写代码内容的格式
否则可能无法正确识别代码块

## 引用
> 这
> 是
> 一
> 段
> 文字
>


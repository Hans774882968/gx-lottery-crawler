[TOC]

## 引言

办公自动化。

## 写入xlsx

### 使用`pandas`写入

安装`pandas`很简单，直接`pip install pandas`。大约占10MB磁盘空间。

根据[pandas documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)，`pd.DataFrame`可以接受dataclass数组，所以我们将`Article`改造为dataclass即可。

```python
from dataclasses import dataclass


@dataclass
class Article:
    date: str
    link: str
    title: str

    def __str__(self) -> str:
        return f'{self.date} {self.link} {self.title}'

    def __eq__(self, value: object) -> bool:
        return self.date == value.date and self.link == value.link and self.title == value.title
```

我们写下这段代码，运行看看效果：

```python
def articles2xlsx(articles: List[Article]):
    df_all = pd.DataFrame(articles)
    duplicate, unq = get_duplicate_and_unique(articles)
    df_unq = pd.DataFrame(unq)
    df_duplicate = pd.DataFrame(duplicate)
    df_arr = (df_all, df_unq, df_duplicate)
    with pd.ExcelWriter('lottery_gx_out.xlsx') as writer:
        for df, sheet_name in zip(df_arr, XLS_SHEET_NAMES):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
```

数据成功写入，但默认的列宽都太小了，需要想办法调大些。

### 使用`styleframe`调整列宽

问了下doubao AI，在用pandas写入excel的场景下，调整列宽是比较麻烦的。之前可用的`set_column`方法已经废弃了（`'Worksheet' object has no attribute 'set_column'`），而现在需要直接导入`openpyxl`：

```python
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from openpyxl import load_workbook

# 创建一个示例DataFrame
data = {'姓名': ['张三', '李四', '王五'],
        '年龄': [20, 25, 30],
        '成绩': [80, 90, 95]}
df = pd.DataFrame(data)

# 将DataFrame写入Excel文件
writer = pd.ExcelWriter('example.xlsx', engine='openpyxl')
df.to_excel(writer, sheet_name='Sheet1', index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']

# 设置列宽
for column in df:
    column_width = max(df[column].astype(str).map(len).max(), len(column))
    col_letter = get_column_letter(df.columns.get_loc(column) + 1)
    worksheet.column_dimensions[col_letter].width = column_width * 1.2
writer.save()
```

因此打算用`styleframe`。只需要`pip install styleframe`。

问了AI（有一个学生列表和一个老师列表。希望生成一个excel文件，将它们分别写入不同的sheet。需要使用Python的pandas和styleframe，且要使用styleframe调整列宽、设置表头样式），注意到`styleframe.StyleFrame`也有一个`to_excel()`方法，在此和`pandas`的`to_excel`一样地调用即可。

```python
from styleframe import StyleFrame

def articles2xlsx(articles: List[Article]):
    # ...
    with pd.ExcelWriter('lottery_gx_out.xlsx') as writer:
        for df, sheet_name in zip(df_arr, XLS_SHEET_NAMES):
            sf = StyleFrame(df)
            sf.set_column_width_dict(
                {
                    'date': 15,
                    'link': 20,
                    'title': 40,
                }
            )
            sf.to_excel(writer, sheet_name=sheet_name, index=False)
```

再打开excel文档，可以看到虽然列宽仍然不够大，但每个单元格的内容都是完整显示的，每一行的文本都居中。这是因为源码里：

```python
# StyleFrame 构造函数有：
self._default_style = styler_obj or Styler()
# 而 Styler 构造函数有：
horizontal_alignment: str = utils.horizontal_alignments.center,
vertical_alignment: str = utils.vertical_alignments.center, # 顺便说下，默认垂直也居中
shrink_to_fit: bool = True
```

接下来我们参考[参考链接2](https://www.cnblogs.com/wang_yb/p/18070891)，给表格多加点样式。

```python
from styleframe import StyleFrame, Styler, utils

def articles2xlsx(articles: List[Article]):
    df_all = pd.DataFrame(articles)
    duplicate, unq = get_duplicate_and_unique(articles)
    df_unq = pd.DataFrame(unq)
    df_duplicate = pd.DataFrame(duplicate)
    df_arr = (df_all, df_unq, df_duplicate)
    with pd.ExcelWriter('lottery_gx_out.xlsx') as writer:
        for df, sheet_name in zip(df_arr, XLS_SHEET_NAMES):
            sf = StyleFrame(df)
            header_style = Styler(
                font_color='#2980b9',
                bold=True,
                font_size=14,
                horizontal_alignment=utils.horizontal_alignments.center,
                vertical_alignment=utils.vertical_alignments.center,
            )
            content_style = Styler(
                font_size=12,
                horizontal_alignment=utils.horizontal_alignments.left,
            )
            sf.apply_headers_style(header_style)
            sf.apply_column_style(sf.columns, content_style)

            # it's a pity that we have to set font_size and horizontal_alignment again
            row_bg_style = Styler(
                bg_color='#bdc3c7',
                font_size=12,
                horizontal_alignment=utils.horizontal_alignments.left,
            )
            indexes = list(range(1, len(sf), 2))
            sf.apply_style_by_indexes(indexes, styler_obj=row_bg_style)

            sf.set_column_width_dict(
                {
                    'date': 15,
                    'link': 20,
                    'title': 40,
                }
            )
            sf.to_excel(writer, sheet_name=sheet_name, index=False)
```

酷！

## 参考资料

1. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
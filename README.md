### ok-script boilerplate

### 使用方法
```
pip install -r requirements.txt #必须使用 python 3.12
python main_debug.py 
```

#### 文件说明
```
src/tasks/ 任务类
src/config.py 项目配置
tests 自动化测试用例
deploy.txt 同步到更新库的文件列表, 如tests文件夹
main.py 入口
main_debug.py debug入口
pyappify.yml 打包配置文件
i18n 国际化文件, 可选
assets cv2使用的template, 需要使用coco格式
.github/workflows/build.yml 自动化构建任务
```

# ok-script 自动化脚本开发指南

本文档旨在帮助开发者了解和使用 `ok-script` 框架来编写自动化任务。我们将通过示例代码详细介绍框架的核心功能。

## 1. Task 的使用

在 `ok-script` 中，所有自动化逻辑都封装在 `Task` 类中。`Task` 分为两种主要类型：**Onetime Task** 和 **Trigger Task**。

### Onetime Task (一次性任务)

`Onetime Task` 继承自 `BaseTask`，它的 `run` 方法只在用户从图形界面点击“运行”时执行一次。它适用于执行有明确开始和结束的流程，例如完成一个每日任务。

**主要特点:**
- **手动触发**: 由用户点击启动。
- **一次性执行**: `run` 方法从头到尾执行一次后即结束。
- **状态管理**: 拥有“运行中”、“已暂停”、“未开始”等状态。

**示例代码:**
```python
import re
from ok import BaseTask

class MyOneTimeTask(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "点击触发运行任务"
        self.description = "用户点击时调用run方法"
        # ... config definitions ...

    def run(self):
        # 自动化逻辑写在这里
        self.log_info('日常任务开始运行!', notify=True)
        self.click(0.47, 0.60)  # 点击屏幕相对坐标 (47%, 60%)
        self.sleep(5)
        self.log_info('日常任务运行完成!', notify=True)
```

### Trigger Task (触发器任务)

`Trigger Task` 继承自 `TriggerTask`，它的 `run` 方法会被框架**循环调用**。它适用于需要持续监控屏幕状态的场景，例如检测到特定界面时自动执行某个操作。

**主要特点:**
- **自动循环**: 启用后，`run` 方法会被反复调用。
- **状态驱动**: 通常在 `run` 方法内通过检查屏幕内容（`ocr` 或 `find_feature`）来决定是否执行具体操作。
- **轻量执行**: `run` 方法应快速返回，避免长时间阻塞，以免影响框架的响应。
- **循环重置**: `run` 方法返回 `True` 时，会重置触发器循环。这可以让其他启用的触发器有机会立即执行，而不是等待当前触发器列表轮询完毕。

**示例代码:**
```python
# file: src/tasks/MyTriggerTask.py
from ok import TriggerTask

class MyTriggerTask(TriggerTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "触发器会不断调用run方法"
        self.description = "一般根据frame来判断是否需要运行"
        self.trigger_count = 0

    def run(self):
        # 每次循环都会执行这里的逻辑
        self.trigger_count += 1
        self.log_debug(f'MyTriggerTask run {self.trigger_count}')
        
        # 示例：如果屏幕上出现“关闭”按钮，就点击它
        if close_button := self.find_one('close_button_feature'):
            self.click_box(close_button)
            # 返回 True 会立即重置触发器队列，让其他触发器优先执行
            return True  
```

---

## 2. Task 中 `config` 的使用

框架提供了强大的配置系统，允许用户在图形界面上调整任务的行为，而无需修改代码。

- **`self.default_config`**: 在 `__init__` 方法中定义一个字典，用于设置默认配置项。这些配置项会自动出现在UI中。
- **`self.config_description`**: (可选) 定义一个字典，为UI中的配置项提供悬浮提示文字。
- **`self.config_type`**: (可选) 用于指定配置项在UI中的显示类型，例如下拉菜单、复选框等。
- **`self.config.get('key')`**: 在 `run` 方法中，使用此方法获取用户设置的当前配置值。

**示例代码:**
```python
class MyOneTimeTask(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "配置使用示例"
        
        # 1. 定义默认配置
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            'list选项': ['第一', '第二', '第3'],
        })

        # 2. (可选) 定义UI描述
        self.config_description.update({
            '是否选项默认支持': '这是一个鼠标悬浮时会显示的提示信息。',
        })

        # 3. (可选) 定义UI类型
        self.config_type.update({
            "下拉菜单选项": {
                'type': "drop_down",
                'options': ['第一', '第二', '第3']
            }
        })

    def run(self):
        # 4. 在代码中获取配置值
        option = self.config.get('下拉菜单选项')
        self.log_info(f'用户选择了: {option}')

        if self.config.get('是否选项默认支持'):
            self.log_info('此选项已被用户启用')
```

---

## 3. `Box` Class 的介绍

`Box` 是一个核心数据结构，用于表示屏幕上的一个矩形区域。所有检测方法（如 `ocr` 和 `find_feature`）的返回值都是 `Box` 对象或其列表。

**主要属性:**
- `x`, `y` (int): 矩形左上角的坐标。
- `width`, `height` (int): 矩形的宽度和高度。
- `name` (str): 识别出的文本内容或特征名称。
- `confidence` (float): 识别的可信度（0.0 到 1.0）。

**常用方法:**
- `box.center()`: 返回 `(x, y)` 格式的中心点坐标元组。
- `box.scale(ratio)`: 返回一个新的 `Box` 对象，其尺寸按比例缩放，中心点不变。
- `box.copy(x_offset, y_offset)`: 返回一个按指定偏移量移动的新 `Box` 对象。
- `box.find_closest_box(direction, boxes)`: 从一个 `Box` 列表中，根据方向 (`'up'`, `'down'`, `'left'`, `'right'`, `'all'`) 找到距离当前 `Box` 最近的另一个 `Box`。

`Box` 对象可以直接传递给 `click_box` 等交互方法。

---

## 4. `template matching` (模板匹配) 相关方法

模板匹配用于在当前屏幕画面中查找预先定义好的小图片（特征）。特征需要在配套的标注工具中进行定义。

- **`self.find_feature(feature_name, box=None, threshold=0.9, ...)`**: 查找指定名称的所有特征。
  - `feature_name` (str | list[str]): 在标注工具中定义的特征名，也支持名称列表。
  - `box` (Box | str): (可选) 限定查找范围，可极大提升速度。可以是 `Box` 对象，也可以是预设的字符串如 `"bottom_right"`。
  - `threshold` (float): (可选) 匹配的相似度阈值，默认为全局配置值。
  - `use_gray_scale` (bool): (可选) 是否使用灰度图进行匹配。
  - `canny_lower`, `canny_higher` (int): (可选) 使用 Canny 边缘检测，并指定低阈值和高阈值。
  - 返回值: `list[Box]`，一个包含所有匹配项的 `Box` 列表。

- **`self.find_one(feature_name, ...)`**: `find_feature` 的便捷版本，只返回可信度最高的那个匹配结果。
  - 返回值: `Box` 或 `None`。

---

## 5. `ocr` (光学字符识别) 相关方法

OCR 用于识别屏幕上的文字。

- **`self.ocr(box=None, match=None, threshold=0.8, ...)`**: 识别指定区域的文字。
  - `box` (Box | str): (可选) 限定识别范围，如 `box="bottom_right"` 或一个 `Box` 对象。这对于提升性能至关重要。也可以直接使用 `x`, `y`, `to_x`, `to_y` 等相对坐标参数定义范围。
  - `match` (str | re.Pattern): (可选) 过滤识别结果，只返回匹配的文本。支持字符串精确匹配和正则表达式模糊匹配。
  - `threshold` (float): (可选) 文字识别的置信度阈值，默认为0.8。
  - `log` (bool): (可选) 是否在日志中打印详细的识别信息和截图，便于调试。
  - `lib` (str): (可选) 指定使用的 OCR 库，默认为 `'default'`。
  - 返回值: `list[Box]`，每个 `Box` 的 `name` 属性是识别出的文本。

**示例:**
```python
def find_some_text_on_bottom_right(self):
    # 在屏幕右下半区寻找“商城”两个字
    return self.ocr(box="bottom_right", match="商城", log=True)

def find_some_text_with_relative_box(self):
    # 使用正则表达式在屏幕右下角 50% 的区域寻找以“招”开头的文字
    return self.ocr(x=0.5, y=0.5, to_x=1, to_y=1, match=re.compile("招"), log=True)
```

---

## 6. `click` (点击) 相关方法

框架提供了多种点击屏幕的方式。

- **`self.click(x, y, ...)`**: 点击指定坐标。
  - 如果 `x`, `y` 是 0.0 到 1.0 之间的小数，则表示相对坐标（屏幕百分比）。
  - 如果是大于 1 的整数，则表示绝对像素坐标。
  - 如果第一个参数是 `Box` 对象, 则会调用 `click_box` 点击该 `Box` 的中心点。
  - `down_time` (float): (可选) 按下和抬起之间的延迟（秒）。
  - `after_sleep` (float): (可选) 点击后等待的时间（秒）。

- **`self.click_box(box, ...)`**: 点击一个 `Box` 对象的中心点。这是最常用的点击方式。
  - `box` (Box | list[Box]): `ocr` 或 `find_one` 返回的 `Box` 对象。如果是列表，则点击第一个元素。
  - `relative_x`, `relative_y` (float): (可选) 点击 `Box` 内部的相对位置，默认为中心 `(0.5, 0.5)`。

- **`self.right_click(...)`, `self.middle_click(...)`**: 执行右键或中键点击，参数与 `self.click` 相同。

- **`self.mouse_down(...)`, `self.mouse_up(...)`**: 单独执行鼠标按下和抬起动作，可用于拖拽。

---

## 7. `wait` (等待) 的相关方法

在自动化流程中，经常需要等待某个元素出现或消失。`wait` 系列方法可以优雅地处理这些等待，避免使用不稳定的 `time.sleep()`。

- **`self.wait_until(condition_func, time_out=10, settle_time=-1, ...)`**: 核心等待方法。它会反复调用 `condition_func` 函数，直到该函数返回一个"真"值（非 `None`、非 `False`、非空列表）或超时。
  - `time_out` (int): 最长等待时间（秒）。
  - `settle_time` (float): (可选) 找到目标后，额外等待一小段时间以确保界面稳定。默认为全局配置值。
  - `raise_if_not_found` (bool): (可选) 如果超时后仍未找到，是否抛出 `WaitFailedException` 异常。

- **`self.wait_feature(feature_name, ...)`**: 等待某个特征出现。
- **`self.wait_click_feature(feature_name, ...)`**: 等待某个特征出现，并点击它。
- **`self.wait_ocr(match, ...)`**: 等待某个文字出现。
- **`self.wait_click_ocr(match, ...)`**: 等待某个文字出现，并点击它。

**示例:**
```python
# 等待“开始战斗”按钮出现，然后点击它，最长等待15秒
# 找到后额外等待0.5秒稳定，点击后暂停1秒
self.wait_click_feature(
    'start_battle_button', 
    time_out=15, 
    settle_time=0.5, 
    after_sleep=1
)
```

---

## 8. 其他交互方法

### `swipe` (滑动)
- **`self.swipe(from_x, from_y, to_x, to_y, duration=0.5, ...)`**: 从一个绝对坐标滑动到另一个绝对坐标。
- **`self.swipe_relative(from_x, from_y, to_x, to_y, ...)`**: 根据屏幕相对坐标进行滑动。

### `scroll` (滚轮)
- **`self.scroll(x, y, count)`**: 在指定绝对坐标位置，滚动鼠标滚轮。`count` 为正数向上，负数向下。
- **`self.scroll_relative(x, y, count)`**: 根据相对坐标滚动。

### `input_text` 和 `send_key` (键盘输入)
- **`self.input_text(text)`**: 输入指定的字符串。
- **`self.send_key(key, down_time=0.02)`**: 发送一个按键事件，例如 `'a'`, `'enter'`, `'f5'`。

---

## 9. 流程控制

- **`self.sleep(seconds)`**: 让任务暂停指定的秒数。在暂停期间，框架仍然可以响应退出信号，比 `time.sleep()` 更安全。
- **`self.next_frame()`**: 强制框架获取并处理下一帧屏幕图像。当你执行一个操作（如点击）后，希望立即获取该操作导致的新画面时，可以调用此方法。

---

## 10. `log` 和 `screenshot` (调试)

调试是开发过程中的重要一环。

- **`self.log_info(message, notify=False)`**: 记录一条普通信息日志。如果 `notify=True`，会在桌面右下角弹出通知。
- **`self.log_debug(message)`**: 记录一条调试信息，仅在调试模式下显示。
- **`self.log_error(message, exception)`**: 记录一条错误信息。
- **`self.screenshot(name)`**: 保存一张当前画面的截图到 `debug` 文件夹，便于分析问题。

---

## 11. 自动化测试

为 `Task` 编写单元测试可以确保其逻辑的正确性，并方便回归测试。

- **测试基类**: 测试用例需要继承 `TaskTestCase`。
- **模拟屏幕**: 使用 `self.set_image('path/to/image.png')` 方法，将屏幕画面固定为一张静态图片，使测试环境保持一致。
- **断言**: 使用 `unittest` 的断言方法（如 `self.assertEqual`）来验证任务方法的返回值是否符合预期。

**示例测试代码:**
```python
# file: tests/test_my_task.py
import unittest
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.MyOneTimeTask import MyOneTimeTask

class TestMyOneTimeTask(TaskTestCase):
    # 指定要测试的 Task 类
    task_class = MyOneTimeTask

    def test_ocr1(self):
        # 1. 设置当前屏幕为一张指定的图片
        self.set_image('tests/images/main.png')
        
        # 2. 调用 task 实例的方法
        text_boxes = self.task.find_some_text_on_bottom_right()
        
        # 3. 断言结果是否符合预期
        self.assertEqual(text_boxes[0].name, '商城')

    def test_ocr2(self):
        self.set_image('tests/images/main.png')
        text_boxes = self.task.find_some_text_with_relative_box()
        self.assertEqual(text_boxes[0].name, '招募')

# 运行测试
if __name__ == '__main__':
    unittest.main()
```
import re

from qfluentwidgets import FluentIcon

from src.tasks.MyBaseTask import MyBaseTask


class MyOneTimeWithAGroup2(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "放在A分组tab里的任务2"
        self.description = "放在不同分组"
        self.group_name = "A分组"
        self.group_icon = FluentIcon.SYNC
        self.icon = FluentIcon.SYNC
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
            'list选项': ['第一', '第二', '第3'],
        })
        self.config_type["下拉菜单选项"] = {'type': "drop_down",
                                      'options': ['第一', '第二', '第3']}

    def run(self):
        self.log_info('放在不同分组tab里的任务!', notify=True)




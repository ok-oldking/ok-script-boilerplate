from ok import ConfigOption

version = "dev"

key_config_option = ConfigOption('Game Hotkey Config', { #全局配置示例
    'Echo Key': 'q',
    'Liberation Key': 'r',
    'Resonance Key': 'e',
    'Tool Key': 't',
}, description='In Game Hotkey for Skills')

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'global_configs': [key_config_option],
    'gui_icon': 'icons/icon.png',
    'wait_until_before_delay': 0,
    'wait_until_check_delay': 0,
    'wait_until_settle_time': 0.2,
    'ocr': {
        'lib': 'onnxocr',
        'params': {
            'use_openvino': True,
        }
    },
    'windows': {  # required  when supporting windows game
        'exe': 'ZenlessZoneZero.exe',
        # 'hwnd_class': 'UnrealWindow', #增加重名检查准确度
        'interaction': 'Genshin', #支持大多数PC游戏后台点击
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        'bit_blt_render_full': True,
        'check_hdr': True, #当用户开启AutoHDR时候提示用户, 但不禁止使用
        'force_no_hdr': False, #True=当用户开启AutoHDR时候禁止使用
        'require_bg': True # 要求使用后台截图
    },
    'start_timeout': 120,  # default 60
    'window_size': { #ok-script窗口大小
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
    'supported_resolution': {
        'ratio': '16:9', #支持的游戏分辨率
        'min_size': (1280, 720), #支持的最低游戏分辨率
        'resize_to': [(2560, 1440), (1920, 1080), (1600, 900), (1280, 720)], #如果非16:9自动缩放为 resize_to
    },
    'analytics': {
        'report_url': 'http://report.ok-script.cn:8080/report', #上报日活, 可选
    },
    'screenshots_folder': "screenshots", #截图存放目录, 每次重新启动会清空目录
    'gui_title': 'ok-script-boilerplate',  # Optional
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'version': version, #版本
    'my_app': ['src.globals', 'Globals'], # 全局单例对象, 可以存放加载的模型, 使用og.my_app调用
    'onetime_tasks': [  # tasks to execute
        ["src.tasks.OneTimeTask", "OneTimeTask"],
        ["ok", "DiagnosisTask"],
    ],
    'trigger_tasks':[
        ["src.tasks.MyTriggerTask", "MyTriggerTask"],
    ]
}

### 语音数据的存储与检索的实现

#### 技术栈
python mongodb

#### python外部包
pymongo numpy pyaudio

#### 概述
程序入口在memory.py中，默认添加aohan（傲寒）lvse（绿色）celian（侧脸）xiaoxingyun（小幸运）hongzhaoyuan（红昭愿），五首歌曲。
测试文件均为record前缀，带有human尾缀的为无旋律人声。
经过测试发现，瓶颈与问题主要在指纹算法，对于旋律敏感，人声歌词不敏感。导致部分人声测试失败，部分旋律成分低的歌曲失败。
指纹算法有待改进。
存储效率检索效率很高，单线程搜索都极快速。
项目已无力维护，2024年7月21日起归档

---

项目石沉大海了，以后更新会很慢

---

## EasyClock
一个简单的学习时钟  
第二十五届郑州市学生信息素养提升实践活动-计算思维类-创意编程-初中组 参赛作品

### 功能介绍/开发计划
 - [x] 基本功能
   - [x] 时间/日期/节日显示
   - [x] 高考倒计时
   - [x] 问候语
   - [x] 一言小语
     - [x] 换一句一言小语
   - [x] 待办列表
 - [ ] 高级功能
   - [ ] 专注模式
     - [ ] 全屏化专注模式
     - [ ] 窗口化专注模式
   - [ ] 设置功能
     - [ ] 自定义字体
     - [ ] 自定义倒计时内容
     - [ ] 自定义主题

### 使用指南
1. 打开下载的安装包
2. 按照提示安装
3. 安装完成
4. 打开软件就可以愉快的使用了！

### 贡献者指南
要想对本仓库进行代码贡献，你需要：Python3.8及以上 + Git  
本项目使用`poetry`进行依赖管理，请参阅[`poetry`官方文档](https://python-poetry.org/docs/)
1. fork本仓库并使用`git clone`命令克隆本仓库到本地
2. 运行`poetry install`来安装依赖（本项目默认使用清华大学、阿里云、北京外国语大学镜像源以提升依赖安装速度）
3. 完成代码编写后提交pr，注意检查代码规范，git提交信息参阅vscode插件git-commit-plugin

### 编译指南
本项目使用`pyinstaller + NSIS`进行python打包及制作安装程序
1. 运行`poetry install`来安装依赖（见贡献者指南）
2. 使用`pyinstaller`打包，注意要将打包后的文件输出到`dist/main/`中，否则NSIS将找不到文件
3. 使用NSIS编译`src/installer.nsi`文件

*注：`installer.nsi`脚本未经测试，可能出现Bug*

### 关于
本软件由ymy139开发  
当前版本：v0.1.0  
使用`Python + PyQt`开发
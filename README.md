[![Extend](https://github.com/mybdye/H/actions/workflows/main.yml/badge.svg)](https://github.com/mybdye/H/actions/workflows/main.yml)
- 建议修改 schedule 
`.github/workflows/main.yml` 中 
```
schedule:
    # UTC (国内 UTC+8)
    - cron: '03 02 */2 * *'   
    # 每2天 10:03am 执行
```
```
规则参考
* * * * *
| | | | |
| | | | +----- day of week (0 - 7) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
| | | +------- month (1 - 12) OR jan,feb,mar,apr ...
| | +--------- day of month (1 - 31)
| +----------- hour (0 - 23)
+------------- minute (0 - 59)
```
#### ✏️
- 10.26
  - add version_main 
- 10.11
  - add URL_BASE，多个网址配置参考 `/.github/workflows/main.yml`
  - fix renewCheck
- 10.09
  - fix 原 speech to text 网站 gg，切换到 Azure
  - add ffmpeg mp3 to wav
  - add renewCheck
- 06.26 
  - 固定版本selenium==4.2.0，原因 4.3.0 * Deprecated find_element_by_* and find_elements_by_* are now removed (#10712) https://github.com/SeleniumHQ/selenium/blob/a4995e2c096239b42c373f26498a6c9bb4f2b3e7/py/CHANGES

#### ㊙️

|YOU SECRET NAME|YOU SECRET VALUE|
|-----|--|
|`URL_BASE_H` or `URL_BASE_W`|网址，至少写一个，不要带有'https://' 或 '/'|
|`USER_ID`|你的 id|
|`PASS_WD`|你的密码|
|`BARK_KEY`|(可选) https://api.day.app/BARK_KEY/|
|`TG_BOT_TOKEN`|(可选) `xxxxxx:xxxxxxxxxxxxx`|
|`TG_USER_ID`|(可选) 给 bot `@userinfobot` 发送 `/start`|

#### 📚
- https://www.python.org/
- https://www.selenium.dev/
- https://www.youtube.com/watch?v=As-_hfZUyIs
- https://github.com/actions/virtual-environments/blob/main/images/macos/macos-12-Readme.md
- https://github.com/mherrmann/selenium-python-helium/blob/master/helium/__init__.py

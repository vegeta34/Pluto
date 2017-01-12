#-*- coding: UTF-8 -*-
__author__ = 'alexkan'

"""
本地执行时的一些配置
"""

PACKAGENAME = "com.wetest.demo"

# Info Server Configurations
info_server_address = "10.205.2.216"  # 正式服10.205.2.216，预发布服10.206.3.27， 测试服10.12.234.150
info_server_port = 8080
target_directory = "upload_screenshot_directory"
info_server_configuration_file = "./config.properties"
local_image_save_path="screenshot"

#ML_SERVER_URL="http://10.24.195.33:8082" #machine learning 服务器地址 预发布服机器IP:10.24.197.42
ML_SERVER_URL="http://10.12.236.236:8082" #machine learning 服务器地址 预发布服机器IP:10.24.197.42local_image_save_path="./screen_images/"


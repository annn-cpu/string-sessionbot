# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 8080 端口
EXPOSE 8080

# 运行机器人
CMD ["python", "string_generator_bot.py"]

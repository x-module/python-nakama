#!/bin/bash

# 添加可执行权限（如果需要）
chmod +x "$GO_SCRIPT"

echo "开始循环执行Go脚本..."

while true; do
    echo "===== 执行开始于 $(date) ====="

    # 执行Go脚本并捕获退出状态
    /Users/tudou/python/python-nakama-v2/.venv/bin/python /Users/tudou/python/python-nakama-v2/example/login.py
    echo "===== 执行结束于 $(date)，退出状态: $EXIT_STATUS ====="

    # 根据需要添加延迟（可选）
    # sleep 1  # 如果需要延迟1秒再执行下一次

    # 如果Go脚本非正常退出（非0），可以选择退出循环
    # if [ $EXIT_STATUS -ne 0 ]; then
    #     echo "Go脚本异常退出，停止循环"
    #     break
    # fi
done

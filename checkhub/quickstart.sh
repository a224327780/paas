#!/bin/bash

# CheckHub 快速启动脚本

echo "=================================================="
echo "     CheckHub 自动签到系统 - 快速启动"
echo "=================================================="
echo ""

# 检查 Python 版本
echo "检查 Python 环境..."
python3 --version

# 检查依赖
echo ""
echo "检查依赖..."
if ! pip list | grep -q "sanic"; then
    echo "依赖未安装，正在安装..."
    pip install -r requirements.txt || {
        echo "依赖安装失败！请手动执行: pip install -r requirements.txt"
        exit 1
    }
fi

# 检查配置文件
echo ""
echo "检查配置文件..."

if [ ! -f "config/sites.toml" ]; then
    echo "创建默认站点配置文件..."
    if [ -f "config/sites.example.toml" ]; then
        cp config/sites.example.toml config/sites.toml
    fi
fi

if [ ! -f "config/settings.toml" ]; then
    echo "创建默认系统设置文件..."
    if [ -f "config/settings.example.toml" ]; then
        cp config/settings.example.toml config/settings.toml
    fi
fi

echo ""
echo "=================================================="
echo "     环境准备完成！"
echo "=================================================="
echo ""
echo "请选择运行模式："
echo ""
echo "1. Web 管理模式 (推荐用于首次配置和可视化管理)"
echo "   运行命令: python run.py"
echo "   访问地址: http://localhost:8000"
echo "   默认账号: admin / admin123"
echo ""
echo "2. 命令行模式 (推荐用于定时任务和自动化)"
echo "   运行命令: python checkin.py"
echo "   查看帮助: python checkin.py --help"
echo ""
read -p "请输入选项 (1 或 2): " choice

case $choice in
    1)
        echo ""
        echo "正在启动 Web 管理模式..."
        python3 run.py
        ;;
    2)
        echo ""
        echo "运行命令行模式..."
        echo ""
        python3 checkin.py --list
        echo ""
        read -p "是否立即执行签到? (y/n): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python3 checkin.py
        else
            echo "使用 'python checkin.py' 命令执行签到"
        fi
        ;;
    *)
        echo ""
        echo "无效选项！"
        echo ""
        echo "手动运行方式："
        echo "  Web 模式: python run.py"
        echo "  命令行模式: python checkin.py"
        ;;
esac

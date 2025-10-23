#!/bin/bash

echo "=================================="
echo "CheckinHub 快速开始"
echo "=================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Python 版本: $PYTHON_VERSION"
echo ""

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
else
    echo "✓ 虚拟环境已存在"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt -q
echo "✓ 依赖安装完成"
echo ""

# 创建配置文件
echo "配置文件检查..."
if [ ! -f "config/config.toml" ]; then
    echo "创建主配置文件..."
    cp config/config.toml.example config/config.toml
    echo "✓ 已创建 config/config.toml"
else
    echo "✓ config/config.toml 已存在"
fi

if [ ! -f "config/sites.toml" ]; then
    echo "创建站点配置文件..."
    cp config/sites.toml.example config/sites.toml
    echo "✓ 已创建 config/sites.toml"
else
    echo "✓ config/sites.toml 已存在"
fi
echo ""

# 创建日志目录
mkdir -p logs
echo "✓ 日志目录已就绪"
echo ""

echo "=================================="
echo "安装完成！"
echo "=================================="
echo ""
echo "下一步："
echo "1. 编辑配置文件："
echo "   nano config/config.toml"
echo "   nano config/sites.toml"
echo ""
echo "2. 查看可用站点："
echo "   python main.py --list"
echo ""
echo "3. 运行签到："
echo "   python main.py"
echo ""
echo "更多信息请查看 README.md"
echo ""

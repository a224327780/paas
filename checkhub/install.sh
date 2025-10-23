#!/bin/bash

echo "🎯 CheckHub 安装脚本"
echo "===================="
echo ""

# 检查Python版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"
echo ""

# 创建虚拟环境
echo "创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
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
echo "安装依赖包..."
pip install -r requirements.txt -q
echo "✓ 依赖安装完成"
echo ""

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p logs data config
echo "✓ 目录创建完成"
echo ""

# 复制配置文件示例
if [ ! -f "config/sites.toml" ]; then
    echo "创建默认配置文件..."
    cp config/sites.toml.example config/sites.toml 2>/dev/null || true
    cp config/settings.toml.example config/settings.toml 2>/dev/null || true
    echo "✓ 配置文件已创建"
else
    echo "✓ 配置文件已存在"
fi
echo ""

# 运行测试
echo "运行基础测试..."
python test_basic.py
echo ""

echo "===================="
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 修改配置文件: config/settings.toml 和 config/sites.toml"
echo "2. 启动应用: python run.py"
echo "3. 访问: http://localhost:8000"
echo ""
echo "默认登录信息："
echo "  用户名: admin"
echo "  密码: admin123"
echo ""
echo "⚠️  请在首次登录后立即修改密码！"
echo ""

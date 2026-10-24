#!/usr/bin/env bash
set -e

# 切换到项目根目录
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "  🚀 正在启动 Agentic RAG 系统"
echo "=========================================="

# 1. 检查并准备环境变量文件
if [ ! -f "project/.env" ] && [ -f "project/.env.example" ]; then
    echo "📄 正在从 project/.env.example 创建 project/.env..."
    cp project/.env.example project/.env
fi

# 2. 检查 Ollama 服务状态
if command -v curl >/dev/null 2>&1; then
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "⚠️  提示：Ollama 似乎未在 localhost:11434 运行。"
        echo "   如果使用默认本地模型，请先运行 'ollama serve'。"
    fi
fi

# 3. 启动应用（优先使用 uv）
if command -v uv >/dev/null 2>&1; then
    echo "⚡ 使用 uv 管理 Python 环境..."
    uv run project/app.py
else
    echo "🐍 未检测到 uv，将使用标准 Python 虚拟环境..."
    PYTHON_CMD=""
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo "❌ 错误：需要 Python 3.11 或更高版本，但未找到 python3 或 python。"
        exit 1
    fi

    if [ ! -d ".venv" ]; then
        echo "🔨 正在 .venv 中创建虚拟环境..."
        $PYTHON_CMD -m venv .venv
    fi

    # 激活虚拟环境
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    elif [ -f ".venv/Scripts/activate" ]; then
        source .venv/Scripts/activate
    fi

    echo "📦 正在检查并安装依赖..."
    pip install -q -r requirements.txt

    echo "🚀 正在启动应用..."
    python project/app.py
fi

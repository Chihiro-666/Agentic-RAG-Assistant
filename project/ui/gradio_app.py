import gradio as gr
from core.chat_interface import ChatInterface
from core.document_manager import DocumentManager
from core.rag_system import RAGSystem
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


def create_gradio_ui():
    rag_system = RAGSystem()
    rag_system.initialize()

    doc_manager = DocumentManager(rag_system)
    chat_interface = ChatInterface(rag_system)

    def format_file_list():
        files = doc_manager.get_markdown_files()
        if not files:
            return "📭 知识库中暂无文档"
        return "\n".join([f"{f}" for f in files])

    def upload_handler(files, progress=gr.Progress()):
        if not files:
            return None, format_file_list()

        added, skipped = doc_manager.add_documents(
            files,
            progress_callback=lambda p, desc: progress(p, desc=desc)
        )

        gr.Info(f"✅ 已添加：{added} 份 | 已跳过：{skipped} 份")
        return None, format_file_list()

    def clear_handler():
        try:
            doc_manager.clear_all()
            gr.Info("🗑️ 已清空所有文档")
        except Exception as exc:
            gr.Error(f"清空文档失败：{exc}")
        return format_file_list()

    def chat_handler(msg, hist):
        for chunk in chat_interface.chat(msg, hist):
            yield chunk

    def clear_chat_handler():
        chat_interface.clear_session()

    with gr.Blocks(title="智能知识库助手") as demo:
        gr.Markdown("# 智能知识库助手\n\n管理文档，并基于知识库进行对话。", elem_id="app-header")

        with gr.Tab("文档管理", elem_id="doc-management-tab"):
            gr.Markdown("## 添加文档")
            gr.Markdown("上传 PDF 或 Markdown 文件。已存在的文档会自动跳过；如需重新建立索引，请先使用“清空全部”。")

            files_input = gr.File(
                label="上传 PDF 或 Markdown 文件",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False
            )

            add_btn = gr.Button("添加文档", variant="primary", size="md")

            gr.Markdown("## 知识库中的文档")
            file_list = gr.Textbox(
                value=format_file_list(),
                interactive=False,
                lines=7,
                max_lines=10,
                elem_id="file-list-box",
                show_label=False
            )

            with gr.Row():
                refresh_btn = gr.Button("刷新列表", size="md")
                clear_btn = gr.Button("清空全部", variant="stop", size="md")

            add_btn.click(upload_handler, [files_input], [files_input, file_list], show_progress="corner")
            refresh_btn.click(format_file_list, None, file_list)
            clear_btn.click(clear_handler, None, file_list)

        with gr.Tab("对话"):
            chatbot = gr.Chatbot(
                height=720,
                placeholder="<strong>你好！</strong><br><em>请提出问题，我会检索知识库并为你整理答案。</em>",
                show_label=False,
                avatar_images=(None, os.path.join(ASSETS_DIR, "chatbot_avatar.png")),
                layout="bubble",
                elem_id="chatbot"
            )
            chatbot.clear(clear_chat_handler)

            gr.ChatInterface(
                fn=chat_handler,
                chatbot=chatbot,
                textbox=gr.Textbox(
                    placeholder="输入问题后按 Enter 发送",
                    show_label=False,
                    submit_btn="发送",
                    stop_btn="停止生成",
                ),
            )

    return demo
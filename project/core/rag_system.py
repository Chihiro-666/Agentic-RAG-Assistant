import json
import uuid
from urllib import request, error

from langchain_ollama import ChatOllama
import config
from db.vector_db_manager import VectorDbManager
from db.parent_store_manager import ParentStoreManager
from document_chunker import DocumentChunker
from rag_agent.tools import ToolFactory
from rag_agent.graph import create_agent_graph
from core.observability import Observability


class RAGSystem:

    def __init__(self, collection_name=config.CHILD_COLLECTION):
        self.collection_name = collection_name
        self.vector_db = VectorDbManager()
        self.parent_store = ParentStoreManager()
        self.chunker = DocumentChunker()
        self.observability = Observability()
        self.agent_graph = None
        self.thread_id = str(uuid.uuid4())
        self.recursion_limit = config.GRAPH_RECURSION_LIMIT
        self.llm_model_name = config.LLM_MODEL

    def _get_ollama_models(self):
        try:
            with request.urlopen("http://localhost:11434/api/tags", timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except error.URLError as exc:
            raise RuntimeError(
                "无法连接到 Ollama（http://localhost:11434）。请启动 Ollama 后重试。"
            ) from exc
        except (ValueError, TimeoutError) as exc:
            raise RuntimeError(f"读取 Ollama 模型列表失败：{exc}") from exc

        models = payload.get("models", []) if isinstance(payload, dict) else []
        return [model.get("name") for model in models if isinstance(model, dict) and model.get("name")]

    def _resolve_ollama_model(self):
        requested_model = config.LLM_MODEL
        available_models = self._get_ollama_models()

        if requested_model in available_models:
            return requested_model

        candidates = [requested_model, *config.OLLAMA_FALLBACK_MODELS]
        for candidate in candidates:
            if candidate in available_models:
                if candidate != requested_model:
                    print(
                        f"提示：未找到请求的 Ollama 模型“{requested_model}”，"
                        f"将改用已安装的模型“{candidate}”。"
                    )
                return candidate

        if available_models:
            fallback = available_models[0]
            print(
                f"提示：未找到请求的 Ollama 模型“{requested_model}”，"
                f"将改用第一个已安装的模型“{fallback}”。"
            )
            return fallback

        raise RuntimeError(
            f"尚未安装任何 Ollama 聊天模型。请在终端运行 `ollama pull {requested_model}`，然后重新启动应用。"
        )

    def initialize(self):
        self.vector_db.create_collection(self.collection_name)
        collection = self.vector_db.get_collection(self.collection_name)

        self.llm_model_name = self._resolve_ollama_model()
        llm = ChatOllama(
            model=self.llm_model_name,
            temperature=config.LLM_TEMPERATURE,
            seed=config.LLM_SEED,
        )
        tools = ToolFactory(collection).create_tools()
        self.agent_graph = create_agent_graph(llm, tools)

    def get_config(self):
        cfg = {"configurable": {"thread_id": self.thread_id}, "recursion_limit": self.recursion_limit}
        handler = self.observability.get_handler()
        if handler:
            cfg["callbacks"] = [handler]
        return cfg

    def reset_thread(self):
        try:
            self.agent_graph.checkpointer.delete_thread(self.thread_id)
        except Exception as e:
            print(f"提示：无法删除会话 {self.thread_id}：{e}")
        self.thread_id = str(uuid.uuid4())

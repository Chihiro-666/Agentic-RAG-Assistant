from langchain_core.tools import tool
import config
from db.parent_store_manager import ParentStoreManager
from core.execution_logger import log_error, log_tool_end, log_tool_start

class ToolFactory:
    
    def __init__(self, collection):
        self.collection = collection
        self.parent_store_manager = ParentStoreManager()
    
    def _search_child_chunks(self, query: str, limit: int = config.DEFAULT_RETRIEVAL_K) -> str:
        """搜索文档片段，查找与用户问题相关的证据。

        将此工具作为第一步检索。结果包含父块 ID、文件名和简短的子块摘录。
        如果摘录相关但过于零散，无法支持可靠回答，则使用返回的 parent_id
        调用 retrieve_parent_chunks。
        
        Args:
            query: 聚焦且包含问题中具体关键词的搜索查询。
            limit: 最多返回的子块数量。
        """
        log_tool_start("search_child_chunks", {"query": query, "limit": limit})
        try:
            results = self.collection.similarity_search(
                query,
                k=limit,
                score_threshold=config.RETRIEVAL_SCORE_THRESHOLD,
            )
            if not results:
                output = "NO_RELEVANT_CHUNKS"
                log_tool_end("search_child_chunks", output)
                return output

            output = config.CHILD_CHUNK_SEPARATOR.join([
                f"父块 ID：{doc.metadata.get('parent_id', '')}\n"
                f"文件名：{doc.metadata.get('source', '')}\n"
                f"内容：{doc.page_content.strip()}"
                for doc in results
            ])
            log_tool_end("search_child_chunks", output)
            return output

        except Exception as e:
            log_error("search_child_chunks", e)
            output = f"RETRIEVAL_ERROR: 检索文档片段失败：{str(e)}"
            log_tool_end("search_child_chunks", output)
            return output
    
    def _retrieve_parent_chunks(self, parent_id: str) -> str:
        """读取相关子块对应的完整父块。

        仅当 search_child_chunks 返回了相关的 parent_id，且子块摘录需要更多上下文时使用。
        不要重复读取压缩上下文中已经包含的父块 ID。
    
        Args:
            parent_id: search_child_chunks 返回的父块 ID。
        """
        log_tool_start("retrieve_parent_chunks", {"parent_id": parent_id})
        try:
            parent = self.parent_store_manager.load_content(parent_id)
            if not parent:
                output = "NO_PARENT_DOCUMENT"
                log_tool_end("retrieve_parent_chunks", output)
                return output

            output = (
                f"父块 ID：{parent.get('parent_id', 'n/a')}\n"
                f"文件名：{parent.get('metadata', {}).get('source', 'unknown')}\n"
                f"内容：{parent.get('content', '').strip()}"
            )
            log_tool_end("retrieve_parent_chunks", output)
            return output

        except Exception as e:
            log_error("retrieve_parent_chunks", e)
            output = f"PARENT_RETRIEVAL_ERROR: 读取父块失败：{str(e)}"
            log_tool_end("retrieve_parent_chunks", output)
            return output
    
    def create_tools(self) -> list:
        """创建并返回工具列表。"""
        search_tool = tool("search_child_chunks")(self._search_child_chunks)
        retrieve_tool = tool("retrieve_parent_chunks")(self._retrieve_parent_chunks)
        
        return [search_tool, retrieve_tool]

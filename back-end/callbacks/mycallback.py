from typing import Dict, Any, List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class MyCallbackHandler(BaseCallbackHandler):
    '''def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any :
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        print(f"\n\n\033[1m> Launching this LLM {class_name}\033[0m")
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("*********")'''

    def __init__(self, tool_name, *args, **kwargs):
        # Initialisation de la classe parent avec tous les paramètres reçus
        super().__init__(*args, **kwargs)
        # Ajout de la logique spécifique à l'enfant avec le nouveau paramètre
        self.tool_name = tool_name

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        print(f"***Réponse du LLM pour {self.tool_name}:***\n{response.generations[0][0].text}")
        print("*********")

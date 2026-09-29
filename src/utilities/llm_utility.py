import json
import boto3
from typing import List
from urllib.parse import quote_plus
import os
from config.config_manager import config
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core import Document
from utilities.bedrock import *



class LLMUtility:

    def __init__(self):
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=config.aws_region,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
        )

    
    
    async def SemanticChunk(self, content: str,embed_model) -> List[str]:
        doc=Document(text=content)
        splitter = SemanticSplitterNodeParser(buffer_size=1,breakpoint_percentile_threshold=30,embed_model=embed_model)
        nodes = splitter.get_nodes_from_documents([doc])

        return nodes


    def generate_embeddings(self,nodes, embed_model):
        """Generate embeddings for each chunk."""
        results = []
        if isinstance(nodes,str):
            return embed_model.get_text_embedding(nodes)
        for node in nodes:
            content = node.get_content()
            
           
            if node.embedding:
                embedding = node.embedding
            else:
                embedding = embed_model.get_text_embedding(content)
            
            results.append(embedding)
        
        return results

   
    #  Build System Prompt
  
    async def build_prompt(self, query: str, context_chunks) -> str:
        
        
        context = "\n\n".join(context_chunks)
        context = context.join(query)

        prompt = fprompt = f"""
<role>
You are an intelligent AI Room Recommendation Assistant.
You must strictly follow the provided instructions.
</role>

<objective>
Your task is to recommend rooms strictly based on the provided context.
You must NOT use any external knowledge.
You must NOT assume missing information.
</objective>



<instructions>

1. Use ONLY the information inside the <context> section.
2. Do NOT generate, assume, infer, or fabricate any information.
3. Do NOT use prior knowledge.
4. Do NOT suggest alternative rooms unless they exist in the provided context.
5. A room is valid ONLY if:
   - It satisfies the requested capacity.
   - It includes ALL requested amenities.
6. If no room satisfies the request, return an empty list [].
7. If the user question is unrelated to room recommendations 
   (e.g., weather, politics, coding, math, personal advice, etc.),
   strictly respond exactly with:

   "Answer":"I don't know."

8. If the context does not contain enough information to answer,
   strictly respond exactly with:

   "Answer":"I don't know."

9. Return the response strictly in valid JSON format.
10. Do NOT return explanations.
11. Do NOT return natural language paragraphs.
12. Do NOT wrap the JSON in markdown.
13. Do NOT include any extra keys.

</instructions>


"""



        return prompt.strip()



    async def invoke_llm(self, prompt: str) -> str:

        body=json.dumps({
            "messages":[
                {
                    "role":"user",
                    "content":[
                        {"text":prompt}
                    ]
                }
            ],
            "inferenceConfig":{
                "maxTokens":400,
                "temperature":0.4
            }
        })

        response = self.bedrock_client.invoke_model(
            modelId=config.llm_model_id,
            body=body,
            contentType='application/json',
            accept='application/json'
        )
        response_body = json.loads(response['body'].read())

        
        return response_body['output']['message']['content'][0]['text']
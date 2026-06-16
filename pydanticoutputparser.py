from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description='Name of the person.')
    age: int = Field(gt=18, description='Age of the person.')
    city: str = Field(description='Name of the city person belongs to')

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template="""
Generate a fictional {place} person.

{format_instruction}

IMPORTANT RULES:
1. Return ONLY JSON.
2. Do NOT explain anything.
3. Do NOT write Python code.
4. Do NOT use markdown.
5. Do NOT use ```json blocks.
6. Output must start with {{
7. Output must end with }}
""",
    input_variables=["place"],
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    }
)

chain = template | model | parser

result = chain.invoke({"place": "indian"})

print(result)

print(type(result))

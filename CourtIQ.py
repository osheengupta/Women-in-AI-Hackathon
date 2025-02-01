# ------------ 1. Install Dependencies ------------
# pip install pymilvus==2.3.3 anthropic gradio python-dotenv numpy

# ------------ 2. Imports & Setup ------------
import os
import numpy as np
import gradio as gr
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ------------ 3. Configuration ------------
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ------------ 4. Sample Data (Fallback) ------------
legal_cases = [
    {
        "text": "Landlords must return security deposits within 30 days of lease termination",
        "year": 2022,
        "embedding": np.random.rand(768).tolist()
    },
    {
        "text": "Employers must provide reasonable accommodations under ADA",
        "year": 2023,
        "embedding": np.random.rand(768).tolist()
    }
]

# ------------ 5. Milvus Setup ------------
connections.connect(host="localhost", port="19530")

# Create collection if not exists
collection_name = "legal_cases"
if not utility.has_collection(collection_name):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
        FieldSchema(name="year", dtype=DataType.INT64),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]
    schema = CollectionSchema(fields, description="Legal Cases")
    collection = Collection(collection_name, schema)
else:
    collection = Collection(collection_name)
    collection.load()

# Insert data if empty
if collection.num_entities == 0:
    try:
        collection.insert([
            [case["text"] for case in legal_cases],
            [case["year"] for case in legal_cases],
            [case["embedding"] for case in legal_cases]
        ])
        collection.load()
    except Exception as e:
        print(f"Insert failed: {str(e)}")

# ------------ 6. RAG Functions ------------
def find_similar_cases(query):
    try:
        results = collection.search(
            data=[np.random.rand(768).tolist()],  # Simplified for demo
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=2,
            output_fields=["text", "year"]
        )
        return [{"text": hit.entity.text, "year": hit.entity.year} for hit in results[0]]
    except Exception as e:
        print(f"Search error: {str(e)}")
        return legal_cases[:2]  # Return sample cases

def generate_summary(query, cases):
    try:
        context = "\n".join([f"- {case['text']} ({case['year']})" for case in cases])
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Explain these legal principles simply:\n{context}"
            }]
        )
        return response.content[0].text
    except Exception as e:
        return f"Summary unavailable: {str(e)}"

# ------------ 7. Gradio Interface ------------
def legal_assistant(query):
    cases = find_similar_cases(query)
    summary = generate_summary(query, cases)
    return f"## Summary\n{summary}\n\n## Relevant Cases\n" + "\n".join(
        [f"{i+1}. {case['text']} ({case['year']})" for i, case in enumerate(cases)]
    )

gr.Interface(
    fn=legal_assistant,
    inputs=gr.Textbox(label="Legal Query"),
    outputs=gr.Markdown(),
    title="⚖️ Legal Assistant Prototype",
    #examples=["Can my landlord keep my deposit?", "What are my ADA rights at work?"]
).launch(share=True)
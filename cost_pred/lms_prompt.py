# %%
import json
import lmstudio as lms

# %%
def dental_cement(cdt_col: str, desc_col: str, model: str = "deepseek/deepseek-r1-0528-qwen3-8b") -> str:

    prompt = f"""For Common Dental Code {cdt_col} with the description "{desc_col}" - would the correct execution of this procedure require the application of dental cement? Please answer either TRUE or FALSE."""
    
    schema = {
      "type": "object"
    , "properties": {
          "thinking": {"type": "string"}
        , "answer": {"type": "string"}}
    , "required": ["thinking", "answer"]}


    with lms.Client() as client:
        model = client.llm.model(model)
        result = model.respond(prompt, response_format=schema)


    return str(result)

# %%
print(dental_cement("D5222", "Immediate mandibular partial denture - resin base (including retentive/clasping materials, rests and teeth)"))
# %%

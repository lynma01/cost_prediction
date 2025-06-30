# %%
import configparser
import os
from google import genai

# %%
def get_gemini_api_key(config_file: str = "../.ini") -> str | None:
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        return None

    config.read(config_file)

    try:
        return str(config.get("gemini", "api_key"))
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error reading API key from '{config_file}': {e}")
        return None

# %%
def determine_product_fit(cdt_col: str, desc_col: str, key: str = get_gemini_api_key()) -> str:

    prompt = f"""
    Your job is to provide two things: 1) a one word response of 'HYDROGEL', 'CROWN', 'BOTH', or 'NONE' based on whether or not a given dental procedure can be successfully substituted with the one, both, or none of the components comprising the UCleaner LLC product, and 2) a summary of your reasoning as to why you provided the answer you did. The response should be formatted in `json` format with the following keys: "response", and "reasoning".
    
    You will be provided with the Common Dental Terminology code (CDT code) and a description of the procedure, and a description of the UCleaner LLC product and some reference information to aid in your determination.

    ## CDT Code to analyze

    - CDT Code: {cdt_col}
    - Description: {desc_col}

    ## UC Cleaner LLC Product:

    The UCleaner LLC product is a tissue-regeneration biologic composed of two parts: 

    1) A biosynthetically derived hydrogel suffused with specific dental growth factors for recruiting stem-cells from the pulp for tissue regeneration in the dentum and/or enamel. This part of the product would replace conventional dental fillings which completely block the movement/recruitment of cells.

    2) An additively-manufactured crown composed of biologically sympathetic ingredients for protecting the exposed pulp or dentum cells within a decayed or damaged tooth. This crown ensures that the recruited stem-cells from the pulp are also able to traverse to the outer-most layer of the teeth, while also protecting the tooth-interior from daily use.

    ### Reference Information:

    The product is meant to be a substitute for the following dental procedures:

    1. Installing crowns
      1.a Amalgam
      2.b Composite
    2. Installing Inlays and/or Onlays
    3. Fillings for living, but damaged/decayed teeth
    4. Multi-coded services requiring both crowns and fillings
    """

    client = genai.Client(api_key=key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    return str(response.candidates[0].content.parts[0].text).replace("```json", "").replace("```", "")
# %%

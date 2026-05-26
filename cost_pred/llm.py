import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent / ".env")


def get_api_key() -> str | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key is None:
        print("Error: ANTHROPIC_API_KEY not found in environment. Check your .env file.")
    return key


def determine_product_fit(cdt_col: str, desc_col: str, key: str | None = None) -> str:
    if key is None:
        key = get_api_key()
    if key is None:
        raise RuntimeError("ANTHROPIC_API_KEY not set.")

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

    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text.replace("```json", "").replace("```", "")

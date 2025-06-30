# %%
import json
import configparser
import os
from google import genai

# %%

def get_gemini_api_key(config_file: str = "../.ini") -> str | None:
    """
    Reads the Gemini API key from a configuration file.

    Args:
        config_file (str): The path to the configuration file.
                           Defaults to 'config.ini'.

    Returns:
        str | None: The API key if found, otherwise None.
    """
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
def dental_cement(cdt_col: str, desc_col: str, key: str = get_gemini_api_key()) -> str:

    prompt = f"""For Common Dental Code {cdt_col} with the description "{desc_col}" - would the correct execution of this procedure require the application of dental cement? Please answer either TRUE or FALSE."""

    client = genai.Client(api_key=key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return str(response.candidates[0].content.parts[0].text)

# %%
print(dental_cement("D5222", "Immediate mandibular partial denture - resin base (including retentive/clasping materials, rests and teeth)"))
# %%

import json
import torch
import numpy as np
from PIL import Image
import google.generativeai as genai

try:
    import openai
except ImportError:
    openai = None

class UltimatePromptVisionary:
    def __init__(self):
        # Base negative prompts for SFW mode
        self.negative_base = "nsfw, (low quality, worst quality:1.2), lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, artist name, messy room, deformed, distorted,"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "llm_engine": (["Gemini", "ChatGPT", "Grok", "Ollama"], {"default": "Gemini"}),
                "api_key": ("STRING", {"default": ""}),
                "base_url": ("STRING", {"default": "http://localhost:11434/v1"}),
                "base_model": ([
                    "SD 1.5 / 2.1", 
                    "SDXL", 
                    "FLUX", 
                    "ZIT", 
                    "PONY", 
                    "Illustrious", 
                    "Qwen2-VL"
                ], {"default": "SDXL"}),
                "role": ([
                    "Game Environment Designer", 
                    "Cinematic Scene Designer", 
                    "Fantasy Architect", 
                    "Realistic Architect", 
                    "Character Concept Artist"
                ], {"default": "Realistic Architect"}),
                "safety_mode": (["SFW", "NSFW"], {"default": "SFW"}),
                "creativity": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "user_note": ("STRING", {"default": "Describe your inspiration...", "multiline": True}),
                "manual_boost": ("STRING", {"default": "8k resolution, cinematic lighting, masterpiece, highly detailed,", "multiline": True}),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("Positive_Prompt", "Negative_Prompt", "Description_Display", "Raw_JSON")
    FUNCTION = "visionary_process"
    CATEGORY = "VisionaryAI"

    def visionary_process(self, llm_engine, api_key, base_url, base_model, role, safety_mode, creativity, user_note, manual_boost, image=None):
        
        # --- 1. Engine Restriction & Safety Logic ---
        actual_safety = safety_mode
        engine_warning = ""
        
        if llm_engine in ["Gemini", "ChatGPT"]:
            if safety_mode == "NSFW":
                actual_safety = "SFW"
                engine_warning = f"⚠️ {llm_engine} does not support NSFW. Switched to SFW mode.\n"

        # --- 2. Base Model Strategies ---
        model_guidelines = {
            "SD 1.5 / 2.1": "Use weighted tags (e.g., (keyword:1.2)), emphasize quality words first, keep it concise and tag-based.",
            "SDXL": "Use a mix of descriptive natural language and tags. Supports complex compositions.",
            "FLUX": "Use long, highly detailed natural language sentences. Describe the scene like a story.",
            "ZIT": "Focus on structured descriptions and technical lighting parameters.",
            "PONY": "MUST start with 'score_9, score_8_up, score_7_up, rating_safe'. Use Danbooru tags.",
            "Illustrious": "Focus on high-end illustrative styles and clean compositions.",
            "Qwen2-VL": "Describe the image with precise object placement and material properties."
        }
        selected_guideline = model_guidelines.get(base_model, "")

        # --- 3. System Prompt Construction ---
        role_map = {
            "Game Environment Designer": "Expert in Unreal Engine 5 style, PBR textures, and dynamic lighting.",
            "Cinematic Scene Designer": "Expert in professional photography: Anamorphic lens, Bokeh, and Color grading.",
            "Fantasy Architect": "Specializes in magical elements, bioluminescence, and epic scales.",
            "Realistic Architect": "Expert in photorealistic architectural rendering (V-Ray/Corona) and interior aesthetics.",
            "Character Concept Artist": "Specializes in character design and unique visual traits."
        }
        
        safety_instruction = (
            "Strictly follow SFW (Safe for Work) guidelines." if actual_safety == "SFW" 
            else "NSFW mode is authorized. Detailed descriptions of anatomical beauty or bold artistic details."
        )
        
        system_instruction = f"""
        Role: {role}
        Expertise: {role_map.get(role, "")}
        Target Image Model: {base_model}
        Strategy: {selected_guideline}
        Constraint: {safety_instruction}
        User Note: "{user_note}"
        
        Output strictly in JSON:
        {{
          "description": "Short summary",
          "positive_prompt": "Optimized prompt for {base_model}",
          "negative_prompt": "Negative keywords"
        }}
        """

        # --- 4. Image Processing ---
        pil_image = None
        if image is not None:
            # Convert ComfyUI Tensor to PIL
            i = 255. * image[0].cpu().numpy()
            pil_image = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # --- 5. LLM Request Branch ---
        try:
            response_text = ""
            
            if llm_engine == "Gemini":
                genai.configure(api_key=api_key)
                
                # Dynamic Model Selection for Gemini 3
                try:
                    available_models = [
                        m.name for m in genai.list_models() 
                        if "generateContent" in m.supported_generation_methods
                    ]
                    # Prioritize Gemini 3 Flash, then 1.5 Flash, then fallback
                    if any("gemini-3-flash" in m for m in available_models):
                        target_model = next(m for m in sorted(available_models, reverse=True) if "gemini-3-flash" in m)
                    else:
                        target_model = next((m for m in sorted(available_models, reverse=True) if "gemini-1.5-flash" in m), "models/gemini-1.5-flash")
                except:
                    target_model = "models/gemini-3-flash-preview"

                model = genai.GenerativeModel(
                    model_name=target_model,
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
                
                content = [system_instruction, pil_image] if pil_image else [system_instruction]
                response = model.generate_content(content)
                
                if response.candidates and response.candidates[0].finish_reason == 3: # SAFETY
                    return ("Safety Blocked", "", "Content blocked by safety filters.", "{}")
                response_text = response.text

            else:
                if openai is None: return ("Missing openai library", "", "pip install openai", "{}")
                client = openai.OpenAI(api_key=api_key, base_url=base_url if llm_engine != "ChatGPT" else None)
                model_name = "gpt-4o" if llm_engine == "ChatGPT" else ("grok-beta" if llm_engine == "Grok" else "llama3")
                
                messages = [{"role": "system", "content": system_instruction}]
                res = client.chat.completions.create(model=model_name, messages=messages, temperature=creativity)
                response_text = res.choices[0].message.content

            # --- 6. Parsing & Composition ---
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            ai_pos = data.get("positive_prompt", "high quality")
            ai_neg = data.get("negative_prompt", "")
            desc = engine_warning + f" [Used: {target_model if llm_engine=='Gemini' else model_name}] " + data.get("description", "")
            
            final_pos = f"{manual_boost} {ai_pos}"
            final_neg = f"{self.negative_base} {ai_neg}" if actual_safety == "SFW" else ai_neg

            return (final_pos, final_neg, desc, clean_json)

        except Exception as e:
            return (f"Error: {str(e)}", "", "API call failed.", json.dumps({"error": str(e)}))

# Mapping
NODE_CLASS_MAPPINGS = { "UltimatePromptVisionary": UltimatePromptVisionary }
NODE_DISPLAY_NAME_MAPPINGS = { "UltimatePromptVisionary": "Ultimate Prompt Visionary (Gemini 3 Ready)" }
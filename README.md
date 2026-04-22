put the folder "ComfyUI-VisionaryAI" at:
ComfyUI_windows_portable\\ComfyUI\\custom_nodes

put the JSON "example_workflow" at:
ComfyUI_windows_portable\\ComfyUI\\user\\default\\workflows



### IMPORTANT
The generated results will inevitably be affected by Checkpoint and LoRA. This node and workflow only provide prompt generation.



Ultimate Prompt Visionary User Manual (v1.1)

This is a high-level AI prompt generation node designed specifically for ComfyUI. It integrates multiple Large Language Models (LLMs) with optimized syntax logic for various base models, transforming simple inspirations into professional-grade Stable Diffusion prompts.

Installation Path
Place the folder ComfyUI-VisionaryAI at:
ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VisionaryAI

Place the JSON file example_workflow at:
ComfyUI_windows_portable\ComfyUI\user\default\workflows

Core Node Parameter Analysis
1. Model and Connection Settings
llm_engine: Select the AI brain to drive the node (Gemini, ChatGPT, Grok, Ollama).

api_key: Enter the API key for the corresponding platform.

base_url: Set this when using Ollama or a proxy server.

base_model (New Feature): The core improvement of V1.1. Select the base model you plan to run in your ComfyUI backend. The node will automatically adjust the AI's prompt generation logic:

SD 1.5 / 2.1: Focuses on weighted tags and keyword-heavy prompts.

SDXL: Uses a mix of descriptive short phrases and tags, ideal for complex compositions.

FLUX: Switches to "Pure Natural Language" descriptions to leverage FLUX's superior semantic understanding.

PONY: Automatically injects specific rating tags like score_9, score_8_up....

Illustrious: Emphasizes high-end illustrative styles and aesthetic descriptions.

Qwen2-VL: Uses visual analysis-style descriptions, focusing on spatial relationships and material properties.

2. Creative Logic Settings
role: Determines the AI's professional terminology preference (e.g., Realistic Architect, Game Environment Designer, Cinematic Scene Designer).

safety_mode:

SFW: Strictly adheres to safety guidelines.

NSFW: Fully released only in Grok or Ollama modes (Gemini/ChatGPT will force a switch back to SFW).

creativity: The higher the value (0.0 ~ 1.0), the richer the AI's imagination, though it may deviate more from the original note.

3. Prompt Enhancement
user_note: Your original inspiration (supports any language including Traditional/Simplified Chinese, English, etc.).

manual_boost: Quality tags that are forcibly appended (default includes 8k resolution, cinematic lighting, etc.).

Workflow Structure Description
A. Prompt Generation Area (Ultimate Prompt Visionary)
Depending on your selected base_model, the output data will vary:

Positive_Prompt: The final positive prompt optimized for the specific model's syntax.

Negative_Prompt: Automatically completed negative prompts based on the architecture and safety settings.

Description_Display: A textual summary of the scene by the AI to verify if it understood your intent correctly.

B. Image Generation and Post-processing
Supports connection to Checkpoint and LoRA for rendering.

The default workflow includes a 4xUpscale process to enhance the details of the final output.

Advanced Operating Techniques
Model-Specific Prompting:
If you find the results underwhelming when using FLUX, ensure the base_model is set to FLUX. This tells the AI to stop stacking keywords and instead use coherent English sentences, which significantly improves FLUX's performance.

Vision Function (Image Analysis):
You can connect an image to the image input. The AI will analyze the image content in conjunction with your user_note. For example: upload a rough sketch and enter "Cyberpunk style"—the AI will accurately describe the composition of the sketch while adding the requested stylistic details.

Troubleshooting
Safety Blocked by Gemini: This means the content triggered Google’s safety filters. Try a milder description or switch engines.

Missing openai library: Please run pip install openai in your terminal.

Syntax Incompatibility: If you see strange score tags at the start of your prompt, check if the base_model is accidentally set to PONY.

<img width="1920" height="960" alt="pic_1" src="https://github.com/user-attachments/assets/7f1f0311-5508-4dfd-b01b-c43a41794836" />

<img width="1920" height="960" alt="pic_2" src="https://github.com/user-attachments/assets/fb0e1ba4-9844-442d-a23c-21bcc918740d" />

<img width="1920" height="960" alt="pic_3" src="https://github.com/user-attachments/assets/26e49a04-1aae-4ae6-b3be-8d237384c4f2" />

<img width="1920" height="960" alt="pic_4" src="https://github.com/user-attachments/assets/9ccfb25d-e933-4ee3-9029-1129e6c74567" />

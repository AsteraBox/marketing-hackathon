import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import time

MODEL_NAME = "IlyaGusev/saiga_mistral_7b"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."

class Conversation:
    def __init__(
        self,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        response_template=DEFAULT_RESPONSE_TEMPLATE
    ):
        self.message_template = message_template
        self.response_template = response_template
        self.messages = [{
            "role": "system",
            "content": system_prompt
        }]

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_bot_message(self, message):
        self.messages.append({
            "role": "bot",
            "content": message
        })

    def get_prompt(self, tokenizer):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += DEFAULT_RESPONSE_TEMPLATE
        return final_text.strip()


def generate(model, tokenizer, prompt, generation_config):
    data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(
        **data,
        generation_config=generation_config
    )[0]
    output_ids = output_ids[len(data["input_ids"][0]):]
    output = tokenizer.decode(output_ids, skip_special_tokens=True)
    return output.strip()

config = PeftConfig.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(
    model,
    MODEL_NAME,
    torch_dtype=torch.float16
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
print(generation_config)

user_input = ""
stop_words = ['stop', 'quit', 'halt']
reset_words = ['new']
print(f"Для очистки диалога введите одну из следующих команд: {reset_words}.\nДля завершения работы используйте любую из команд: {stop_words}")
while user_input not in stop_words:
    print("==============================")
    conversation = Conversation()
    while True:
        user_input = input("User: ")
        if user_input in stop_words + reset_words:
            break
        start_time = time.time()
        conversation.add_user_message(user_input)
        prompt = conversation.get_prompt(tokenizer)
        output = generate(model, tokenizer, prompt, generation_config)
        print(f"Saiga ({time.time() - start_time} s): {output}\n")


#inputs = ["Почему трава зеленая?", "Сочини длинный рассказ, обязательно упоминая следующие объекты. Дано: Таня, мяч"]
#for inp in inputs:
#    conversation = Conversation()
#    conversation.add_user_message(inp)
#    prompt = conversation.get_prompt(tokenizer)

#    output = generate(model, tokenizer, prompt, generation_config)
#    print(inp)
#    print(output)
#    print()
#    print("==============================")
#    print()


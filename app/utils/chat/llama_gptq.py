from transformers import AutoTokenizer, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig


pretrained_model_dir = "facebook/opt-125m"
quantized_model_dir = "opt-125m-4bit"


tokenizer = AutoTokenizer.from_pretrained(pretrained_model_dir, use_fast=True)
examples = [
    tokenizer(
        "auto-gptq is an easy-to-use model quantization library with user-friendly apis, based on GPTQ algorithm."
    )
]

# quantize_config = BaseQuantizeConfig(
#     bits=4,  # quantize model to 4-bit
#     group_size=128,  # it is recommended to set the value to 128
# )

# # load un-quantized model, by default, the model will always be loaded into CPU memory
# model = AutoGPTQForCausalLM.from_pretrained(pretrained_model_dir, quantize_config)

# # quantize model, the examples should be list of dict whose keys can only be "input_ids" and "attention_mask"
# model.quantize(examples, use_triton=False)

# # save quantized model
# model.save_quantized(quantized_model_dir)

# # save quantized model using safetensors
# model.save_quantized(quantized_model_dir, use_safetensors=True)

# load quantized model to the first GPU
model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir, device="cuda:0", use_triton=False)

# inference with model.generate
print(tokenizer.decode(model.generate(**tokenizer("auto_gptq is", return_tensors="pt").to("cuda:0"))[0]))

# # or you can also use pipeline
# pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer)
# print(pipeline("auto-gptq is")[0]["generated_text"])

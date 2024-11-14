from transformers import pipeline

class Translator:
    def __init__(self):
        self.model = pipeline("translation_en_to_fr", model="t5-small", device='cuda')
        
    def translate(self, text: str) -> str:
        model_output = self.model(text)
        translation = model_output[0]['translation_text']
        return translation
    
translator = Translator()
translation = translator.translate("good morning")
print(translation)


#py-spy, opencensus-context, mpmath, distlib, colorful, wrapt, websockets, uvloop, urllib3, uc-micro-py, typing-extensions, tqdm, sympy, sniffio, six, safetensors, rpds-py, regex, pyyaml, python-dotenv, pygments, pyasn1, protobuf, propcache, prometheus-client, platformdirs, packaging, nvidia-nvtx-cu12, nvidia-nvjitlink-cu12, nvidia-nccl-cu12, nvidia-curand-cu12, nvidia-cufft-cu12, nvidia-cuda-runtime-cu12, nvidia-cuda-nvrtc-cu12, nvidia-cuda-cupti-cu12, nvidia-cublas-cu12, numpy, networkx, msgpack, mdurl, MarkupSafe, idna, httptools, h11, grpcio, fsspec, frozenlist, filelock, exceptiongroup, click, charset-normalizer, certifi, cachetools, attrs, async-timeout, annotated-types, aiohappyeyeballs, virtualenv, uvicorn, triton, smart-open, rsa, requests, referencing, pydantic-core, pyasn1-modules, proto-plus, nvidia-cusparse-cu12, nvidia-cudnn-cu12, multidict, markdown-it-py, linkify-it-py, jinja2, googleapis-common-protos, anyio, aiosignal, yarl, watchfiles, starlette, rich, pydantic, nvidia-cusolver-cu12, mdit-py-plugins, jsonschema-specifications, huggingface-hub, google-auth, torch, tokenizers, jsonschema, google-api-core, fastapi, aiohttp, transformers, textual, ray, opencensus, aiohttp-cors, memray
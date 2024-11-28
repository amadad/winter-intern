import ollama

for chunk in ollama.chat(
    model='llama3.2-vision:90b',
    messages=[{
        'role': 'user',
        'content': 'provide an analysis of content of the image',
        'images': ['img/beyond.png']
    }],
    stream=True
):
    print(chunk['message']['content'], end='', flush=True)
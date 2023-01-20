import openai
import os
from flask import Flask, request




app = Flask(__name__)


    
def generate_paragraphs(input_string,max_words):
    openai.api_key = "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"
    
    input_prompt = 'write a storybook with the title:' + input_string

    
    completer = openai.Completion.create(
        model="text-davinci-003",
        prompt= input_prompt,
        max_tokens=max_words,
        temperature=0
)
    
   
    response = completer.choices[0]
    generated_text = response.text

    paragraphs = generated_text.split('\n\n')
    return paragraphs[1:]

def generate_dalle_prompts(input_list):
    openai.api_key = "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"

    dalle_prompts = []
    for input_string in input_list:
        input_prompt = 'please create a DALLE prompt for:' + input_string
        completer = openai.Completion.create(
        model="text-davinci-003",
        prompt= input_prompt,
        max_tokens=20,
        temperature=0
    )
        
        response = completer.choices[0]
        generated_text = response.text
        dalle_prompts.append(generated_text)
    
    return dalle_prompts

def generate_images(dalle_prompts):
    openai.api_key = "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"

    illus = []
    for dalle_prompt in dalle_prompts:
        images = openai.Image.create(
        prompt=dalle_prompt,
        n=1,
        size="1024x1024"
            )
        
        generated_image = images.data[0].url
        illus.append(generated_image)
    
    return illus


@app.route('/',methods = ['GET'])  

def storybook():
    paragraphs = generate_paragraphs(request.args['Prompt'],200)
    prompts = generate_dalle_prompts(paragraphs)
    images = generate_images(prompts)
    pages = {}
    for i in range(len(images)):
        entry = [paragraphs[i], images[i]]
        pages[i] = entry

   
    
    return pages
        

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    




















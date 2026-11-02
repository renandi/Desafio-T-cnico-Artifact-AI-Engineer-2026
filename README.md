

Running the project:

```bash
uv pip install -r requirements.txt
```



I started developing in a Jupyter Notebook because it's easier to debug and analyse the code. After I tested, I chose to implement the code in Python files instead of Jupyter Notebooks to make it more modular.

At first I was running LM Studio with `Qwen 3.5 - 9b` locally, but then I had to switch to OpenAI API instead of local models because semantic search is more powerful than running locally and I was getting some unwanted results with local models. For example the local model could not find the address when I asked in a slightly different expression ("Onde fica a loja física?" - "Where is the physical store?").

I used Gemini's help to guide me through this challenge, as well as a deeplearning.ai course on Retrieval Augmented Generation.

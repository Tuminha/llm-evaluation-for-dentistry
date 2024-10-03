# 🦷 LLM Evaluation for Dentistry: The Quest for the Perfect Dental AI 🧠

Welcome to my exciting journey in the world of Language Models and Dentistry! This repository is part of my quest to find the perfect LLM that knows everything about dentistry, a crucial component of the Periospot AI project.

## 🎯 Project Overview

This project focuses on evaluating various Large Language Models (LLMs), specifically different implementations of LLaMA 3.1 70B, to determine their effectiveness in understanding and generating dental knowledge. It's a fun and intriguing exploration into the intersection of artificial intelligence and dentistry.

### 🧪 What's Inside

This repository contains:

1. `rag_evaluation_test.ipynb`: A Jupyter notebook for testing Retrieval-Augmented Generation (RAG) using OpenAI and Groq APIs.
2. `run_evals.ipynb`: A notebook for running evaluations on different LLaMA 3.1 70B implementations across various providers.
3. Custom evaluation metrics and prompts tailored for dental scenarios.

## 🚀 Getting Started

To dive into this dental AI adventure:

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Copy the `.env.example` file to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Then, open the `.env` file and add your API keys:
   - Add your Weights & Biases API key to `WANDB_API_KEY`
   - Add your OpenRouter API key to `OPENROUTER_API_KEY`
   - Add your Groq API key to `GROQ_API_KEY`
   - Add your Together API key to `TOGETHER_API_KEY`
   - Add your OpenAI API key to `OPENAI_API_KEY`
4. Run the Jupyter notebooks to see the evaluations in action

## 🦷 Why Dentistry and AI?

Dentistry is a complex field with vast amounts of specialized knowledge. By leveraging the power of LLMs, we aim to create an AI assistant that can:

- Assist dental professionals in diagnosis and treatment planning
- Provide instant access to up-to-date dental research
- Help patients understand complex dental procedures

## 🧠 The Quest for the Perfect Dental LLM

Our journey involves:

1. Evaluating LLaMA 3.1 70B implementations from various providers:
   - OctoAI
   - Novita
   - DeepInfra
   - Fireworks
   - Groq
   - Together
2. Creating dental-specific prompts and test cases
3. Analyzing model performance on dental terminology and concepts
4. Comparing the performance of different LLaMA 3.1 70B implementations

Stay tuned for exciting discoveries and dental AI breakthroughs!

## 📊 Evaluation Results

(You can add a brief summary of your findings here, or link to a more detailed results page)

## 🛠️ Tools Used

- Weights & Biases for experiment tracking and visualization
- Python for scripting and data processing
- Jupyter Notebooks for interactive development
- OpenAI API for embeddings and baseline comparisons
- OpenRouter API for accessing various LLaMA 3.1 70B implementations
- Groq API for fast inference
- Together API for additional LLaMA 3.1 70B implementation

## 🙏 Acknowledgements

A huge thank you to the dental community for their expertise and to the AI researchers pushing the boundaries of what's possible with language models. Special thanks to the teams behind LLaMA, OpenAI, Groq, Together, and all the providers offering LLaMA 3.1 70B implementations.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📬 Contact

If you're as excited about the intersection of AI and dentistry as I am, let's connect!

### Contact Information

- **Name:** Francisco Teixeira Barbosa
- **Email:** cisco@periospot.com
- **Personal Portfolio:** [https://franciscodds.framer.ai/](https://franciscodds.framer.ai/)
- **GitHub:** [https://github.com/Tuminha](https://github.com/Tuminha)
- **Twitter/X:** [@Cisco_research](https://x.com/Cisco_research)

Let's revolutionize dentistry with AI! 🦷🤖

# CourtIQ: AI-Powered Legal Assistant 🚀⚖️

CourtIQ is an AI-powered legal assistant that helps bridge the justice gap by making legal help more accessible. Built during the Women in AI RAG Hackathon at Stanford University (where it won 2nd place! 🏆), CourtIQ helps users understand their legal rights and find relevant legal precedents.
Link to blog - here

## Problem Statement 🎯
The "Justice Gap" refers to the disparity between legal needs and resources available, where individuals fail to pursue legal action due to:
- Lack of awareness of their rights
- Fear of the legal system
- Limited access to qualified legal help

## Solution 💡
CourtIQ simplifies the process of understanding your legal rights with Retrieval Augmented Generation (RAG):
1. Input: Users can ask legal questions in plain English (e.g., "My landlord is not returning my deposit")
2. Search: Using Milvus vector database, CourtIQ finds relevant cases from the Caselaw Access Project database
3. Explain: Using LLMs, it provides clear, actionable summaries of the legal principles

## Tech Stack 🛠️
- **Vector Database**: Milvus by Zilliz for storing and searching case embeddings
- **Language Model**: Claude 3 (Haiku) for generating summaries and explanations
- **Frontend**: Gradio for the user interface
- **Dataset**: Caselaw Access Project embeddings for legal precedents
- **Python Libraries**: pymilvus, anthropic, gradio, python-dotenv, numpy

## Getting Started 🚀

### Prerequisites
```bash
pip install pymilvus==2.3.3 anthropic gradio python-dotenv numpy
```

### Environment Setup
Create a `.env` file in the root directory:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### Running the Application
1. Start Milvus server
2. Run the application:
```bash
python attorney.py
```

## Features ✨
- **Quick Case Profiling**: Analyzes user queries to understand legal context
- **Relevant Case Search**: Uses vector similarity to find similar historical cases
- **Clear Explanations**: Converts legal jargon into plain language
- **Lawyer Matching**: Connects users with relevant legal professionals

## Sample Usage 📝
```python
Legal Query: "My landlord is not returning my deposit"

Output:
1. Summary of relevant legal principles
2. Applicable cases and precedents
3. Plain language explanation of rights
4. Next steps and recommendations
```

## Project Structure 📂
```
├── CourtIQ.py          # Main application file
├── .env                 # Environment variables
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Future Roadmap 🗺️
- [ ] Add multimodal data (video legal proceedings)
- [ ] Enhanced lawyer matching filters (cost, success rate, location)
- [ ] Case journey preview generation

## Team 👥
- Prachi Sethi
- Osheen Gupta
- Daniella Pontes

*Note: This is a prototype developed during a hackathon. For production use, additional security measures and error handling would be needed.*

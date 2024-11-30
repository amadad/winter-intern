<div align="center">

<img width="100px" src="./misc/logo.png" />

# Document Analysis System

A flexible system for analyzing legal and business documents using Ollama with the qwq model.

## Overview

This system processes documents to analyze relationships, terms, and agreements between multiple entities. It's designed to be flexible and can handle various types of document analysis tasks.

## Features

- Interactive configuration
- Multi-entity document analysis
- Custom query support
- Automated response generation
- Markdown report generation
- Real-time streaming responses

## Setup

1. Install Ollama and the qwq model:
```bash
# Install Ollama (macOS)
brew install ollama

# Pull qwq model
ollama pull qwq
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Place your documents in the `doc/` directory:
- Any markdown (.md) files you want to analyze
- Example: contracts, agreements, correspondence, etc.

## Usage

1. Run the analysis:
```bash
python main.py
```

2. Follow the interactive prompts:
   - Enter the entities involved
   - Specify the core objective
   - Provide document paths
   - Add custom queries (optional)

3. The script will:
   - Process all documents
   - Generate responses for default and custom queries
   - Save analysis to markdown files in the `out/` directory

## Default Queries

The system includes these default queries:
1. Document differences analysis
2. Payment terms structure
3. IP rights protection
4. Document structure and relationships

You can add custom queries during runtime.

## Output

Analysis results are saved in the `out/` directory as markdown files with timestamps:
```
out/
  └── analysis_YYYYMMDD_HHMMSS.md
```

## Customization

- Modify default queries in `main.py`
- Adjust context window size
- Change output format
- Add new analysis sections

## License

MIT License. See [LICENSE](https://opensource.org/license/mit/) for more information.
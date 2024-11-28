# Document Analysis System

A system for analyzing legal documents and generating responses using Ollama with the qwq model.

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
- `msa.md`: Master Service Agreement
- `sow.md`: Statement of Work
- `bar.md`: Client Contract
- `response.md`: Correspondence

## Usage

Run the analysis:
```bash
python qwq.py
```

The script will:
1. Process and analyze all documents using the qwq model
2. Generate responses for key questions about:
   - Document differences and conflicts
   - Payment terms alignment
   - IP rights protection
   - MSA vs SOW structure

## Customization

To modify the analysis queries, edit the `queries` list in `qwq.py`.
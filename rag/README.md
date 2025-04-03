# Usage

## Making the .env file

Make an .env file in the rag folder with the following content:

```env
DATASET_PATH=path/to/your/dataset/for/rag/enrichment
```


Ensure that you are inside the rag folder

```bash
cd rag
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py --interactive
```

## Testing

Run tests in the whole project root:

```bash
pytest rag/tests
```

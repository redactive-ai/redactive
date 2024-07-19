# Redactive Python SDK

The Redactive Python SDK provides a robust and intuitive interface for interacting with the Redactive platform, enabling developers to seamlessly integrate powerful data redaction and anonymization capabilities into their Python applications.

## Building the Python SDK

`cd sdks/python`

`python -m pip install --upgrade build`

`python -m build`

`python install -e .`

## Building the optional reranker

`cd sdks/python`

`pip install -e ".[reranker]"`

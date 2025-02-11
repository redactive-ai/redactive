# Redactive Permissions Enforcer Client Python SDK

## Installation

Currently supported vector databases include:

- [OpenSearch](https://github.com/opensearch-project/opensearch-py)

```shell
pip install --upgrade redactive-enforcer[opensearch]
```

Install all supported vector database clients with:

```shell
pip install --upgrade redactive-enforcer[all]
```

## Usage

### OpenSearch

Effortlessly enable permissions-enforced queries by utilising the `insert_email_filter()` method before calling the
OpenSearch client.

```python
from opensearchpy import OpenSearch
from redactive_enforcer.opensearch import insert_email_filter


user_email = "jane.doe@redactive.com"
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': 'miller',
      'fields': ['title^2', 'director']
    }
  }
}

# Insert an email-filter into the query body
body = insert_email_filter(body=query, email=user_email)

client = OpenSearch(...)
client.search(body=body, index=...)
```

The process can be simplified by using the `OpenSearch` class exposed by `redactive-enforcer`; a thin child class of
`opensearchpy.OpenSearch` class that modifies only the `search()` method.

```python
from redactive_enforcer.opensearch import OpenSearch

user_email = "jane.doe@redactive.com"
client = OpenSearch(...)
client.search(email=user_email, body=..., index=...)
```

The field name of the ACLs stored in your OpenSearch database can be explicitly set with both methods. Useful for when
ACLs are being stored in a custom field.

```python
from redactive_enforcer.opensearch import OpenSearch, insert_email_filter

# Explicitly define ACL field name for filtering
body = insert_email_filter(body=..., email=..., field_name="custom-field-name")

# Set ACL field name for all subsequent calls of `client.search()`
client = OpenSearch(...)
client.acl_field_name = "custom-field-name"
```

from typing import Any

from redactive_enforcer.hashing import hash_email_preserve_domain

try:
    import opensearchpy
except ModuleNotFoundError:
    raise RuntimeError("opensearchpy is not installed. install with 'redactive-enforcer[opensearch]'")

ACL_FIELD_NAME: str = ...  # TODO pick our redactive default ACL field name out of a hat

def insert_email_filter(body: dict[str, Any] | None, email: str, field_name = ACL_FIELD_NAME) -> dict[str, Any]:
    """
    Returns given OpenSearch search query body with an inserted filter for email against OpenSearch field storing ACLs.

    :param body: The OpenSearch search query body.
    :param email: An email address to insert filter into OpenSearch search query body.
    :param field_name: The field name storing ACLs.
    """
    hashed_email = hash_email_preserve_domain(email)
    _filter = {"term": {field_name: hashed_email}}

    if body is None:
        return {"query": {"bool": {"filter": [_filter]}}}
    elif "query" not in body:
        body["query"] = {"bool": {"filter": [_filter]}}
        return body
    elif "bool" not in body["query"]:
        body["query"] = {"bool": {"must": body["query"], "filter": [_filter]}}
    elif "filter" not in body["query"]["bool"]:
        body["query"]["bool"]["filter"] = [_filter]
    else:
        body["query"]["bool"]["filter"].append(_filter)
    return body


class OpenSearch(opensearchpy.OpenSearch):
    acl_field_name: str = ACL_FIELD_NAME

    def search(
        self,
        *args,
        email: str,
        body: Any = None,
        index: Any = None,
        params: Any = None,
        headers: Any = None,
        **kwargs,
    ) -> Any:
        _body = insert_email_filter(body=body, email=email, field_name=self.acl_field_name)
        return super().search(*args, body=_body, index=index, params=params, headers=headers, **kwargs)
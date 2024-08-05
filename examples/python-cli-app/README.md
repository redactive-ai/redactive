# Redactive Test App

[![PyPI - Version](https://img.shields.io/pypi/v/redactive-test-app.svg)](https://pypi.org/project/redactive-test-app)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/redactive-test-app.svg)](https://pypi.org/project/redactive-test-app)

This sample app can be used to connect to the Redactive platform. With this aopp you can connect to different datasources including Jira, Confluence, Slack, and Sharepoint. Once connected you can then query these sources using Redactive semantic search.

---

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Usage

### Connecting a Datasource

| Datasource   | Id             | Status  |
| ------------ | -------------- | ------- |
| Jira         | `jira`         | stable  |
| Confluence   | `confluence`   | stable  |
| Sharepoint   | `sharepoint`   | stable  |
| Google Drive | `google-drive` | stable  |
| Slack        | `slack`        | stable  |
| Zendesk      | `zendesk`      | preview |

First, create an application API key on the [dashboard](https://dashboard.redactive.ai) and save in your shell as `$REDACTIVE_API_KEY`. Take note of the `redirect_uri`.

```bash
# Datasources can be jira | confluence | google-drive | sharepoint | slack | zendesk

redactive_test_app setup-datasource \
    --app-key=${REDACTIVE_APP_KEY} \
    --datasource="jira" \
    --host="https://api.redactive.ai"
```

This will setup a URL to create an OAuth connection between Redactive and the datasource. Go to the URL and consent to connecting Redactive.

Once this is done the consent page will redirect to the pre-defined `redirect_url`, by default this is `https://url-debugger.vercel.app/` but can be anything. After the redirect is loaded copy the `code` url parameter and paste it back into the console. The app will then finish use this code to obtain an `access_token` and `refresh_token`.

> Note for Zendesk connections you must also specify the `--endpoint` flag. This tells Redactive which subdomain to use to connect to Zendesk with as there is no global authentication endpoint.
>
> ```bash
> redactive_test_app setup-datasource \
>    --app-key=${REDACTIVE_APP_KEY} \
>    --datasource="zendesk" \
>    --endpoint="d3v-redactive-ai" \
>    --host="https://api.redactive.ai"
> ```

### Query an Index

Once you have connected at least one datasource you can now run a semantic search on the index. From steps above save the `access_token` as the environment variable `TOKEN` in your shell.

To run a query enter the following in your shell. The app will then use the Redactive SDK to run semantic search.

```bash
redactive_test_app query \
    --credential $TOKEN \
    --count 3 \
    --host grpc.redactive.ai \
    --port 443
```

This will return a list of chunks that can be used. The `--count` flag is the number of chunks to return from the index.

You can also search a specific datasource by specifying `--datasource`

```bash
redactive_test_app query \
    --credential $TOKEN \
    --count 3 \
	--datasource "jira" \
    --host grpc.redactive.ai \
    --port 443
```

## Installation

It's advised to use the `devcontainer` or `virtual env` to run this app.

Please make sure you have a copy of `redactive-0.0.5-py3-none-any.whl` in the root directory of this project. (We're in the process of uploading to PyPi)

```console
pip install .
```

After the app is installed you can run `redactive_test_app` and start querying!

## License

`redactive-test-app` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

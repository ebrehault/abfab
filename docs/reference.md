# AbFab reference

## Client-side

### Data API

### Fetch API

## Server endpoints

## GitHub webhook

```yaml
on:
    push:
        branches:
            - main
jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - name: Call AbFab webhook
              uses: distributhor/workflow-webhook@v2
              env:
                  webhook_url: 'https://my-domain/_utils/pull/my-app'
                  webhook_secret: 'no-secret'
```

You can choose another branch than `main` by changing the `on.push.branches` value and adding it in the webhook URL:

```yaml
on:
    push:
        branches:
            - prod
jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - name: Call AbFab webhook
              uses: distributhor/workflow-webhook@v2
              env:
                  webhook_url: 'https://my-domain/_utils/pull/my-app/prod'
                  webhook_secret: 'no-secret'
```

## Syncing utility

```sh
docker run --rm -v /<absolute_path>/tutorial:/app/tutorial ebrehault/abfab-utils python utils/sync.py down tutorial --auth root:<password> --host https://demo.abfab.dev/somepath --root . --contents
```

```sh
docker run --rm -v /<absolute_path>/tutorial:/app/tutorial ebrehault/abfab-utils python utils/sync.py up tutorial --auth root:<password> --host https://demo.abfab.dev/somepath/ --root . --contents
```

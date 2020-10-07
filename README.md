# ipmon
Usage is rather simple. Use `cron` to run this script periodically. Update the following with your
own information. `ALLOWLIST` contains the interfaces which must be reported. You can get this
information using `ip a` or `ifconfig`.

```python
IPINFO_FILEPATH = "/home/user/.ipinformation"
ALLOWLIST = ["mynetiface1", "mynetiface2", "mynetiface3"]
ERROR_FILEPATH = "/home/user/.ipinformation.error"
SLACK_WEBHOOK = "https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/6c7e4003b173e3d0c062e850"
```

Refer the following guide from Slack for help on Webhooks.

> https://api.slack.com/messaging/webhooks

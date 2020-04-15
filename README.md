# pstf2
## Passive Security Tools Fingerprinting Framework

Have you ever wanted a simple, easy and stealth bypass for multiple classes of security products? pstf2 is an implementation of an HTTP server capable of passive browser fingerprinting - and it might just be the thing you are looking for.
When attackers try to deliver a payload over the internet they need to overcome multiple tools capable of scanning incoming links. Email filters, scanning engines and even submission to sandbox over URL - all can be bypassed once pstf2 detects them in a passive fashion. Once detected, the tool allows to differentiate between security services and potential victims and deliver either a malicious or benign response.

## Running pstf2
### Getting p0f
Before deploying pstf2, download and install p0f. It is currently available at:

[https://lcamtuf.coredump.cx/p0f3/](https://lcamtuf.coredump.cx/p0f3/)

Now, properly configure lib/servers/server_config.yml to point at the correct path, i.e.:
```
p0f_config:
  # change your username at the very least, remember to change in both paths
  p0f_bin_path: '/Users/$your_user_name/$more_folders/web_fp/p0f-3.09b/p0f'
  p0f_fp_path: '/Users/$your_user_name/$more_folders/web_fp/p0f-3.09b/p0f.fp'
  iface: 'lo0'
  p0f_named_socket: '/tmp/p0f_socket'
```

Also verify that _iface_ is the same interface running your Python HTTP server. In the above example it is the loopback interface.

### Starting the Server

Ocne requirements are satisfied, run:
```
python driver.py
```

You should see output similar to the following:
```
2020-04-15 17:37:06,896 - pstf2_logger - INFO - Starting p0f...
2020-04-15 17:37:06,896 - pstf2_logger - INFO - Running command:
	/Users/gbitensk/work/web_fp/p0f-3.09b/p0f -i lo0 -s /tmp/p0f_socket -f /Users/gbitensk/work/web_fp/p0f-3.09b/p0f.fp
2020-04-15 17:37:06,898 - pstf2_logger - INFO - p0f started!
2020-04-15 17:37:06,898 - pstf2_logger - INFO - Starting HTTP server...
2020-04-15 17:37:06,898 - pstf2_logger - INFO - HTTP server started!
2020-04-15 17:37:06,899 - pstf2_logger - INFO - If you wish to terminate the server press CTRL+C

```

Terminate the server by pressing Ctrl+C, it should terminate the server and the p0f process as well.
You will see something similar too:
```
2020-04-15 17:37:48,263 - pstf2_logger - INFO - HTTP server stopped!
2020-04-15 17:37:48,263 - pstf2_logger - INFO - Killing p0f...
2020-04-15 17:37:48,263 - pstf2_logger - INFO - p0f killed!
2020-04-15 17:37:48,263 - pstf2_logger - INFO - exiting...
```

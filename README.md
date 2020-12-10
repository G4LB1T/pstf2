# pstf^2
## Passive Security Tools Fingerprinting Framework
Have you ever wanted a simple, easy and stealth bypass for multiple classes of security products? pstf^2 (pronounced pstf-square) is an implementation of an HTTP server capable of passive browser fingerprinting - and it might just be the thing you are looking for.
When attackers try to deliver a payload over the internet they need to overcome multiple tools capable of scanning incoming links. Email filters, scanning engines and even submission to sandbox over URL - all can be bypassed once pstf2 detects them in a passive fashion. Once detected, the tool allows to differentiate between security services and potential victims and deliver either a malicious or benign response.

This tool was released during BlackHat EU 2020:
https://www.blackhat.com/eu-20/arsenal/schedule/#pstf2-link-scanners-evasion-made-easy-21763

Details about the research are available in this blog post:
https://blogs.akamai.com/sitr/2020/12/evading-link-scanning-security-services-with-passive-fingerprinting.html

### How it Works?
The real question is - how link scanners work? Inspecting a malicious link is an action involving web client sending an HTTP GET request. Each vendor uses a different in-house implementation - most trying to mimic a real user interaction to some extent.
pstf^2 is a simple python-based HTTP servers which applies well-known bot detection tactics to determine whether an incoming request is from an automated security tool.
The server's operator can customize responses, e.g. - if a scanner is detected redirect to Google otherwise send malicious content.

Below are the main tactics implemented as part of pstf^2:
#### Application Layer
##### Obsolete User Agents
Security tools try to hide as legitimate clients, impersonating real browsers, nevertheless - usually this is not the case.
It is common to see tools which are not maintained properly using fake user-agent headers for browser versions which are a decade old.
pstf^2 allows you to set a minimal threshold for what you consider as a real non-obsolete version.
##### General HTTP Anomalies
There are many types of odd implementations the tool is capable of detecting.
A couple of examples which were presented in the BlackHat talk were:
- Leaving a `via:` header which disclosed the nature of the virtual host used for sandboxing.
- `referer:` header which suggested that the link was reached from Google, e.g. `referer: google.com/search?q=specific.site.com`. 
in the scenarios we tested it made no sense since this product scans emails and when someone clicks an email (not from a web interface) this header is absent.
#### Link, Network and Transportation Layer
##### Correlation
Multiple TCP parameters can imply either a specific OS version or a specific flavour. Some clients spoof the user-agent header but are running on top of an OS different than the one they declare. 
##### MTU Values
Clients hosted on specific cloud providers networks have MTU different than the standard value of 1500 bytes. 
##### ASN
In some cases the request is sent from an ASN associated explicitly with a specific security vendor. In others the request's origin is a cloud hosting provider, while not incriminating a specific vendor it is unlikely to be a typical user.   
##### DNS PTR Records
In rare cases the client's IP address has a PTR record, associating it with URL related to a security vendor.
## Setting up pstf^2
### Using Docker
Assuming you have Docker already installed, it is as simple as that:
```
docker-compose up 
```
### Manual Deployment
In case you wish to avoid Docker, follow these steps.
#### Satisfy Python Requirements
run:
```
pip install requirements.txt
```
This will install any external Python modules required.
#### Getting p0f
Before deploying pstf^2, download and install p0f. It is currently available at:

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

Also verify that `iface` is the same interface running your Python HTTP server. In the above example it is the loopback interface.
#### Running pstf^2
Once requirements are satisfied, run:
```
python driver.py
```
You may use any of the following flags:
```
  --p0f_bin_path P0F_BIN_PATH
  --p0f_fp_path P0F_FP_PATH
  --p0f_iface P0F_IFACE
```
All are used for adjusting parameters related to p0f: the binary itself, the fingerprinting file and the interface we use which defaults to `eth0`.

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
Terminate the server by pressing Ctrl+C, it will kill both the HTTP and p0f instances.
You should see something similar too:
```
2020-04-15 17:37:48,263 - pstf2_logger - INFO - HTTP server stopped!
2020-04-15 17:37:48,263 - pstf2_logger - INFO - Killing p0f...
2020-04-15 17:37:48,263 - pstf2_logger - INFO - p0f killed!
2020-04-15 17:37:48,263 - pstf2_logger - INFO - exiting...
```
Note that setting a DNS record pointing a URL to point at your server is beyond the scope of pstf^2 and at your own responsibility.
### Payload Management
pstf^2 has default payloads which are defined within `server_config.yml` and can be customized with ease.
#### Benign Response
There are two modes, switched by altering the `rickroll_mode` variable for either `YES` or `NO`.
If it is enabled the security tool will be redirected to a YouTube page with the famous [Rickrolling movie](https://en.wikipedia.org/wiki/Rickrolling), otherwise it will serve a string defined in the same YAML file. 
#### Malicious Response
By default - "malicious" response was set to the [EICAR standard testing string](https://www.eicar.org/?page_id=3950).
## Why is pstf^2 Public?
I opted for publicly releasing this tool as an open source project since:
* Malicious links are being used by bad guys on daily basis, in large scale.
* Security tools are not good enough, some of the methods illustrated by pstf^2 are abused in-the-wild.

As part of the tool's construction it was tested against 15 different products, all failed. While I did responsibly disclose details about the attack we still have a long way to go and my expectations is that by making the tool public we will raise the awareness to those tactics which are already being abused by "bad guys".

##### Special Thanks
[@Den1al](https://github.com/Den1al) for providing advice when building this tool specifically, and writing Python properly in general as well as assisting in creating it as a Docker image.

# hCaptcha-Solver-Dumper
Solves and outputs the requestKey for hCaptcha using 2Captcha.
This method requires a **2Captcha api key** since writing a solver is impossible at this stage. 
It basically requires a human to solve it.

# Important Note
This **does not** submit the Captcha for you since most websites use Cloudflare for their Captcha.
How does this effect us? Well, it encrypts the requestKey whenever submitting it.
```
Recently Cloudflare changed the way of processing hCpatcha tokens after solving the captcha. Now tokens are not sent as plain text inside HTTP request to the back-end as it was before. Now tokens are encrypted with the javascript callback function before sending.

Source: https://2captcha.com/blog/hcaptcha-cloudflare-en
```
The issue with encrypting our own tokens is that it requires JavaScript injection which is beyond my knowledge.
I want to keep this project in Python and Python only.
2Captcha recently released a **Google Chrome Plugin** that is able to *"emulate"* this encryption for you, but the code is not open-sourced (I haven't found it online).
Sadly we will have to wait for a method to be released for this, I will keep doing my research around this topic to figure out a solution.

![Image of Dumper](https://i.imgur.com/zujikvu.png)

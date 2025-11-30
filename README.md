Problem:
In the initial days, you don’t get much visibility on your profile. Also, if you’ve deployed your website on Streamlit, it keeps going into sleep mode.

Solution:
My idea is to build a simple backend automation service that periodically visits the website. We can use a Chromium browser with a Selenium script that automatically opens the page and clicks the required button to keep the site active.
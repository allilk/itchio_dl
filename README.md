# itchio_dl
Download your entire itchio bundle

* This will ONLY work on games that have been claimed/added to your library.

1. You need to get your authentication token, and your unique id for the bundle.
2. You need a wget binary, or wget installed

Your authentication token will be in your browser's cookies, just open up devtools and find the cookie "itchio", copy and paste it with the flag "--token (token here)"

Your unique id is what trails your download page on the bundle download view page.

Example command:

`py download.py --token TOKEN --bundle_key UNIQUE_ID`


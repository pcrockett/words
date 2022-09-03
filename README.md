## Words

Having fun with encoding / decoding things using (mostly) English words, and [one-time pad][3] cryptography.

To create a one-time pad, run `make`. Then to see the proof-of-concept:

```bash
echo "hello , this is a dumb message" | ./encrypt.py
# Output: despise anybody customize sedation chastise matrimony jiffy took

echo "despise anybody customize sedation chastise matrimony jiffy took" | ./decrypt.py
# Output: hello , this is a dumb message
```

### Credits

I sourced a lot of my words from:

* [The EFF long word list][1]
* [This nice person's 1000 most common words][2]
* [Ubuntu's `wamerican-small` package][4]

[1]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
[2]: https://gist.github.com/deekayen/4148741
[3]: https://en.wikipedia.org/wiki/One-time_pad
[4]: https://packages.ubuntu.com/jammy/wamerican-small

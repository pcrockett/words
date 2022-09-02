## Words

Having fun with encoding / decoding things using (mostly) English words, and one-time-pad cryptography.

To create a one-time pad, run `make`. Then to see the proof-of-concept:

```bash
echo "hello , this is a dumb message" | ./encrypt.py
# Output: despise anybody customize sedation chastise matrimony jiffy took

echo "despise anybody customize sedation chastise matrimony jiffy took" | ./decrypt.py
# Output: hello , this is a dumb message
```

### Credits

* Word list adapted from [the EFF long word list][1] and [this nice person's 1000 most common words][2].

[1]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
[2]: https://gist.github.com/deekayen/4148741

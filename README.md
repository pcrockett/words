## Words

Having fun with [one-time pad][1] (OTP) cryptography.

**TOY PROJECT!** Don't take anything here seriously.

### Basic Usage

_Only tested on Linux._

---

Generate your one-time pad:

```bash
make
```

---

Encrypt a message:

```bash
echo "Holy cow, Batman!" | ./encrypt.py
```

This outputs something like...

```plaintext
0 spectrum crazily remix omega began
```

If you were to encrypt the same phrase again, it would generate different output that looks something like...

```plaintext
5 dizziness regalia mortally thrift blunt
```

---

Decrypt a message:

```bash
echo "0 spectrum crazily remix omega began" | ./decrypt.py
echo "5 dizziness regalia mortally thrift blunt" | ./decrypt.py
```

This outputs...

```plaintext
holy cow , batman !
holy cow , batman !
```

### Why Did I Do This?

Because it's great nerd fun.

I like simple things that are also effective. You don't need to be a cryptographer to comprehend how one-time pads work.
Yet one-time pads are theoretically unbreakable (assuming you use them correctly), which is more than we can say for
most other encryption algorithms.

Plus one-time pads are feasible to use with pencil and paper, and require little to no math. You can send and receive
messages offline without the help of a computer, for example.

Aside from the fact that I find OTPs _interesting_, I'm also scratching an itch: Most resources you see on the Internet
about one-time pads are concerned about encrypting symbols `A` through `Z`. I find that annoying:

* I don't want to crawl through a message and encrypt / decrypt each individual character. I'm much faster when dealing
  with whole words.
* Whole words are easier to communicate and record in a less error-prone manner. You could reasonably read out an
  encrypted message over the phone, for example.

### What's Left To Do?

Probably just let this sit and rot on GitHub for eternity. Just because you _build_ something doesn't mean you need to
_use_ it or maintain it...

As it currently stands, the pad is pseudorandom because it relies on `/dev/urandom`. This means that this implementation
is still technically vulnerable.

It would be cool to write a tool that assists in generating a _truly_ random one-time pad. One could theoretically write
a script that accepts manual dice rolls as input, and generates a one-time pad that uses the dice rolls as a source of
randomness. All you would need then is boatloads of patience and a few hours to roll dice.

### Credits

Some words in my word list were selected by me, however I sourced the majority of my words from these sources:

* [The EFF short and long word lists][2]
* [This nice person's 1000 most common words][3]

[1]: https://en.wikipedia.org/wiki/One-time_pad
[2]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
[3]: https://gist.github.com/deekayen/4148741

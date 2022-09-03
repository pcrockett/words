## Words

Having fun with [one-time pad][1] (OTP) cryptography.

**TOY PROJECT!** Don't take anything here seriously.

### Basic Usage

Only tested on Linux.

```bash
# Create your one-time pad:
make

echo "Holy cow bat man !" | ./encrypt.py
# Output: truck influential interfere derivations cheating rivalling

echo "truck influential interfere derivations cheating rivalling" | ./decrypt.py
# Output: holy cow bat man !
```

The two scripts also keep track of where they are in the one-time pad, so they won't re-use parts of it. Which means:

* If you encrypt the same phrase several times, the output will be different each time.
* You need to decrypt _everying_ you encrypt, _in order_. Otherwise, the two scripts will get out of sync and you will
  lose the ability to decrypt. _Side note: There is a built-in mechanism to help detect and prevent this situation._

If your scripts get out of sync, it's easy to fix by re-generating the one-time pad:

```bash
rm otp.txt
make
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

I sourced a lot of my words from:

* [The EFF long word list][2]
* [This nice person's 1000 most common words][3]
* [Ubuntu's `wamerican-small` package][4]

[1]: https://en.wikipedia.org/wiki/One-time_pad
[2]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
[3]: https://gist.github.com/deekayen/4148741
[4]: https://packages.ubuntu.com/jammy/wamerican-small

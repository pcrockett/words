.PHONY: sort-wordlist reset-offsets

default: otp.txt

wordlist-sorted.txt: wordlist.txt
	sort --unique --stable wordlist.txt > wordlist-sorted.txt

wordlist-numbered.txt: wordlist-sorted.txt
	nl ./wordlist-sorted.txt > wordlist-numbered.txt

reset-offsets:
	rm -f .otp-encrypt-offset .otp-decrypt-offset

otp.txt: wordlist-numbered.txt reset-offsets
	shuf --repeat \
		--random-source /dev/urandom \
		--head-count 400000 \
		wordlist-numbered.txt \
		> otp.txt

sort-wordlist: wordlist-sorted.txt
	cp wordlist-sorted.txt wordlist.txt

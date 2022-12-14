.PHONY: sort-wordlist test-raw-data

default: otp.txt

wordlist-sorted.txt: wordlist.txt
	sort --unique --stable wordlist.txt > wordlist-sorted.txt

wordlist-numbered.txt: wordlist-sorted.txt
	nl --starting-line-number 0 ./wordlist-sorted.txt > wordlist-numbered.txt

otp.txt: wordlist-numbered.txt
	shuf --repeat \
		--random-source /dev/urandom \
		--head-count 400000 \
		wordlist-numbered.txt \
		> otp.txt
	rm -f .otp-encrypt-offset .otp-decrypt-offset

sort-wordlist: wordlist-sorted.txt
	cp wordlist-sorted.txt wordlist.txt

test-raw-data:
	git log | gzip | base64 | ./encrypt.py \
		| ./decrypt.py | tr --delete [:space:] | base64 --decode | gunzip

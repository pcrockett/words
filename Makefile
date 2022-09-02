default: otp.txt

wordlist-sorted.txt: wordlist-symbols-65536.txt
	sort --unique --stable wordlist-symbols-65536.txt > wordlist-sorted.txt

wordlist-numbered.txt: wordlist-sorted.txt
	nl ./wordlist-sorted.txt > wordlist-numbered.txt

otp.txt: wordlist-numbered.txt
	shuf --repeat \
		--random-source /dev/urandom \
		--head-count 400000 \
		wordlist-numbered.txt \
		> otp.txt

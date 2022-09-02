otp.txt:
	shuf --repeat \
		--random-source /dev/urandom \
		--head-count 400000 \
		wordlist-symbols-65536.txt \
		> otp.txt

.PHONY: run
run:
	cd Ephesus && python main.py

.PHONY: show_hist
show_hist:
	cd Ephesus && python histgram.py
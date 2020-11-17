.PHONY: run
run:
	cd Ephesus && python main.py

.PHONY: hist
hist:
	cd Ephesus && python histgram.py

.PHONY: rerun
rerun:
	rm data/movie_similarity.npy && cd Ephesus && python similarity.py && python main.py
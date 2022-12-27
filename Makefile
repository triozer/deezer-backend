all:
	for d in level*; do \
		(cd $$d; python main.py); \
	done
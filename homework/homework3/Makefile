all: gen analysis

gen: market_sim.py
#	python market_sim.py 1000000 examples/orders-short.csv myout_order_values.csv
	python market_sim.py 1000000 examples/orders.csv myout_order_values.csv
	python market_sim.py 1000000 examples/orders2.csv myout_order2_values.csv

analysis: analyze.py
	python analyze.py myout_order_values.csv "\$$SPX"

	python analyze.py myout_order2_values.csv "\$$SPX"

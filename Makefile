# --- Makefile ---

# define default variables, these can be easily changed when running the program 
ORIGIN = "Porto Campanha"
DEST = "Lisboa Santa Apolonia"
DATE = "20/11/2025"

run:
	@echo "-- Starting Scraper --"
	@echo "Running with ORIGIN=$(ORIGIN), DEST=$(DEST), DATE=$(DATE)"
	
# sets the environment variables
	@ORIGIN=$(ORIGIN) DEST=$(DEST) DATE=$(DATE) python3 main.py

# prettier
help:
	@echo "Usage: make [target] [VARIABLE='value']"
	@echo ""
	@echo "Targets:"
	@printf "  %-20s %s\n" "run" "Run the scraper with specified variables."
	@printf "  %-20s %s\n" "help" "Show this help message."
	@echo ""
	@echo "Variables:"
	@printf "  %-20s %s\n" "ORIGIN" "The departure station."
	@printf "  %-20s %s\n" "DEST" "The arrival station."
	@printf "  %-20s %s\n" "DATE" "The departure date."
	@echo ""
	@echo "Example:"
	@echo "  make run ORIGIN='Faro' DEST='Lisboa - Oriente'"
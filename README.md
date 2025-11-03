# finance_terminal  
Finance and sports analytics terminal CLI and web interface project.  

## Installation  
1. Clone this repository and navigate into the project directory.  
2. Run `setup.sh` to create a virtual environment and install dependencies. Alternatively, create a virtual environment manually and install requirements from `requirements.txt`.  
3. (Optional) run `python3 test_system.py` to perform a quick system test.  

## Usage  
The CLI uses positional arguments in the form `<module> <symbol> <action>`. Modules represent asset classes and actions specify the type of output.  

### Modules  
- `stocks` – interact with stock tickers.  
- `etfs` – interact with exchange‑traded funds.  
- `commodities` – interact with commodity symbols (e.g., gold, oil).  
- `compare` – compare multiple instruments from any supported module. Accepts a comma‑separated list of symbols.  

### Actions  
- `summary` – display a textual summary of the asset(s).  
- `chart` – display a price chart over the past year (supported for stocks, ETFs and compare).  
- `metrics` – show performance metrics such as return and volatility.  

### Examples  
```bash  
python3 main.py stocks AAPL summary  
python3 main.py etfs SPY chart  
python3 main.py commodities gold metrics  
python3 main.py compare AAPL,SPY,GLD chart  
```

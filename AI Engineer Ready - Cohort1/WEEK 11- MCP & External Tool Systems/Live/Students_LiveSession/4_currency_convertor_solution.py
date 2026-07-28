# ============================================================================
# 4_currency_convertor_solution.py -- ONE of FOUR independent MCP servers in
# this demo. Owns the currency_convertor tool: converts an amount between
# currencies using a fixed demo exchange-rate table (not live rates). Run this
# file on its own (python 4_currency_convertor_solution.py); it starts an HTTP
# server on port 8004 that the client (5_multi_server_client_solution.py)
# talks to over MCP/SSE. This was the week's practice challenge.
# ============================================================================

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CurrencyServer", host = "127.0.0.1", port = "8004")

EXCHANGE_RATES_TO_USD = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.0104,
    "JPY": 0.0067,
}

# @app.get("/user"): #fastapi
# def app_users()
# FastMCP -> exposes the functions to LLMs and AI agents through MCP.

@mcp.tool() # This Python function should be exposed as a tool that an AI model can discover and execute
def currency_convertor(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount of money from one currency to another.
    
        Use this whenever the user asks to convert or compare an amount between
        currencies, e.g. "convert 50 USD to INR". Uses fixed demo exchange rates,
        not live rates. Supported currency codes: USD, EUR, GBP, INR, JPY.
    
        Args:
            amount: how much money to convert
            from_currency: 3-letter currency code to convert FROM, e.g. "USD"
            to_currency: 3-letter currency code to convert TO, e.g. "INR"
    """

    from_code = from_currency.strip().upper()
    to_code = to_currency.strip().upper()

    if from_code not in EXCHANGE_RATES_TO_USD or to_code not in EXCHANGE_RATES_TO_USD:
            return {"error": f"Unsupported currency. Supported codes: {list(EXCHANGE_RATES_TO_USD)}"}

    usd_amount = amount * EXCHANGE_RATES_TO_USD[from_code]
    converted = usd_amount / EXCHANGE_RATES_TO_USD[to_code]
    return {
          "amount": amount,
          "from_currency": from_code,
          "to_currency": to_code,
          "converted_amount": round(converted, 2)
    }

if __name__ == "__main__":
      mcp.run(transport = "sse")
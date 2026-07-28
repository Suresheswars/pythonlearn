# ============================================================================
# 4_currency_convertor_student.py -- ONE of FOUR independent MCP servers in
# this demo. Owns the currency_converter tool -- this week's
# 🎯 PRACTICE CHALLENGE. Build it yourself using the hints below.
# ============================================================================

# TODO: from mcp.server.fastmcp import FastMCP

# TODO: create the server -- FastMCP("CurrencyServer", host="127.0.0.1", port=8004)

# TODO: define EXCHANGE_RATES_TO_USD, a dict of fixed demo rates,
# e.g. {"USD": 1.0, "EUR": 1.08, "GBP": 1.27, "INR": 0.012, "JPY": 0.0067}


# TODO: write currency_converter(amount: float, from_currency: str,
# to_currency: str) -> dict, decorated with @mcp.tool()
# hint: normalize both currency codes with .strip().upper() before lookup
# hint: return a clear {"error": ...} dict if either code isn't in your rates table
# hint: convert via USD as the pivot -- amount * rate[from] gives USD, then
# divide by rate[to] to reach the target currency
# hint: round the converted amount (e.g. round(x, 2))
# hint: write a docstring an LLM could read to know exactly when/how to call
# this tool, including which currency codes are supported

# extend-it ideas: more currencies, live rates via an API, return the
# exchange rate used alongside the converted amount


# TODO: under if __name__ == "__main__": call mcp.run(transport="sse")
# (same SSE pattern as 1_calculator_student.py)

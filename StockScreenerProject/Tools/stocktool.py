from langchain.tools import tool
import yfinance as yf
import json 

@tool
def simple_screener(screen_type:str, offset:int)->str:
    """Returns screened assets (stocks, funds, bonds) given popular criteria. 

    Args:
        screen_type: One of a default set of stock screener queries from yahoo finance. 
        aggressive_small_caps
        day_gainers
        day_losers
        growth_technology_stocks
        most_actives
        most_shorted_stocks
        small_cap_gainers
        undervalued_growth_stocks
        undervalued_large_caps
        conservative_foreign_funds
        high_yield_bond
        portfolio_anchors
        solid_large_growth_funds
        solid_midcap_growth_funds
        top_mutual_funds
      offset: the pagination start point

    Returns:
        The a JSON output of assets that meet the criteria
        """
    # query=yf.PREDEFINED_SCREENER_QUERIES[screen_type]['query']
    # result=yf.screen(query,offset=offset,size=5)


    # with open('output.json', 'w') as f: 
    #       json.dump(result, f) 
     
    # fields = ["shortName","bid","ask","exchange", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "averageAnalystRating", "dividendYield", "symbol"] 
    # output_data = []

    # for stock_detail in result['quotes']:
    #      details=[]
    #      for key, val in stock_detail.items():
    #           if key in fields:
    #                details[key]=val

    #      output_data.append(details)
    
    # return f"Stock Screener Results: {output_data}"
    query = yf.PREDEFINED_SCREENER_QUERIES[screen_type]['query']
    result = yf.screen(query, offset=offset, size=5)

    # Iterates over each stock in the screener results.

    # Extracts only the fields you care about (name, bid/ask, exchange, etc.).

    # Builds a clean list of dicts (output_data) with just those fields.

    fields = [
        "shortName", "bid", "ask", "exchange",
        "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
        "averageAnalystRating", "dividendYield", "symbol"
    ]
    output_data = []
    for stock_detail in result['quotes']:
        details = {k: v for k, v in stock_detail.items() if k in fields}
        output_data.append(details)

    return f"Stock Screener Results: {output_data}"

if __name__ == '__main__':
    # Correct way to call a LangChain tool
    result = simple_screener.invoke({"screen_type": "day_gainers", "offset": 0})
    print(result)

# Stock Screener Results: [{'bid': 42.06, 'ask': 42.24, 'exchange': 'NMS', 'fiftyTwoWeekHigh': 90.22, 
#                           'fiftyTwoWeekLow': 40.69, 'averageAnalystRating': '2.1 - Buy', 'shortName': 
#                           'Zillow Group, Inc.', 'symbol': 'ZG'}, {'bid': 42.54, 'ask': 43.32, 'exchange': 'NMS', 
#                         'fiftyTwoWeekHigh': 93.88, 'fiftyTwoWeekLow': 41.135, 'averageAnalystRating': '2.6 - Hold', 
#                         'shortName': 'Zillow Group, Inc.', 'symbol': 'Z'}, {'bid': 201.76, 'ask': 203.05, 'exchange': 'NMS', 
                                                                            
#     'fiftyTwoWeekHigh': 388.14, 'fiftyTwoWeekLow': 192.87, 'averageAnalystRating': '1.6 - Buy', 'dividendYield': 0.59, 'shortName': 'Wingstop Inc.', 
#     'symbol': 'WING'}, {'bid': 271.86, 'ask': 272.79, 'exchange': 'NMS', 'fiftyTwoWeekHigh': 309.9, 'fiftyTwoWeekLow': 28.83, 'averageAnalystRating': '1.6 - Buy', 
#                         'dividendYield': 0.18, 'shortName': 'Western Digital Corporation', 'symbol': 'WDC'}, {'bid': 64.75, 'ask': 65.35, 'exchange': 'NYQ', 
# 'fiftyTwoWeekHigh': 65.5, 'fiftyTwoWeekLow': 31.63, 'averageAnalystRating': '1.4 - Strong Buy', 'shortName': 'Vista Energy S.A.B. de C.V.', 'symbol': 'VIST'}]
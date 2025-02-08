window.onload = function () {
    const spinnerOne = document.querySelector('.flex-item #spinnerOne');
    spinnerOne.style.display = 'block';

    const script1 = document.createElement("script");
    script1.type = "text/javascript";
    script1.src =
        "https://s3.tradingview.com/external-embedding/embed-widget-timeline.js";
    script1.async = true;

    const widgetConfig1 = {
        feedMode: "all_symbols",
        isTransparent: false,
        displayMode: "regular",
        width: "100%",
        height: "100%",
        colorTheme: "dark",
        locale: "en",
    };

    script1.innerHTML = JSON.stringify(widgetConfig1);

    const div1 = document.getElementById("widgetOne");
    if (div1) {
        div1.appendChild(script1);
    }

    script1.onload = function() {
        spinnerOne.style.display = 'none';
    };



    // ====== WIDGET 2 start ======
    const spinnerTwo = document.querySelector('.flex-item #spinnerTwo');
    spinnerTwo.style.display = 'block';

    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src =
        "https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js";
    script.async = true;

    const widgetConfig = {
        title: "Cryptocurrencies",
        title_raw: "Cryptocurrencies",
        tabs: [
            {
                title: "Overview",
                title_raw: "Overview",
                symbols: [
                    { s: "CRYPTOCAP:TOTAL" },
                    { s: "BITSTAMP:BTCUSD" },
                    { s: "BITSTAMP:ETHUSD" },
                    { s: "FTX:SOLUSD" },
                    { s: "BINANCE:AVAXUSD" },
                    { s: "COINBASE:UNIUSD" },
                ],
                quick_link: {
                    title: "More cryptocurrencies",
                    href: "/markets/cryptocurrencies/prices-all/",
                },
            },
            {
                title: "Bitcoin",
                title_raw: "Bitcoin",
                symbols: [
                    { s: "BITSTAMP:BTCUSD" },
                    { s: "COINBASE:BTCEUR" },
                    { s: "COINBASE:BTCGBP" },
                    { s: "BITFLYER:BTCJPY" },
                    { s: "CME:BTC1!" },
                ],
                quick_link: {
                    title: "More Bitcoin pairs",
                    href: "/symbols/BTCUSD/markets/",
                },
            },
            {
                title: "Ethereum",
                title_raw: "Ethereum",
                symbols: [
                    { s: "BITSTAMP:ETHUSD" },
                    { s: "KRAKEN:ETHEUR" },
                    { s: "COINBASE:ETHGBP" },
                    { s: "BITFLYER:ETHJPY" },
                    { s: "BINANCE:ETHBTC" },
                    { s: "BINANCE:ETHUSDT" },
                ],
                quick_link: {
                    title: "More Ethereum pairs",
                    href: "/symbols/ETHUSD/markets/",
                },
            },
            {
                title: "Solana",
                title_raw: "Solana",
                symbols: [
                    { s: "FTX:SOLUSD" },
                    { s: "BINANCE:SOLEUR" },
                    { s: "COINBASE:SOLGBP" },
                    { s: "BINANCE:SOLBTC" },
                    { s: "HUOBI:SOLETH" },
                    { s: "BINANCE:SOLUSDT" },
                ],
                quick_link: {
                    title: "More Solana pairs",
                    href: "/symbols/SOLUSD/markets/",
                },
            },
            {
                title: "Uniswap",
                title_raw: "Uniswap",
                symbols: [
                    { s: "COINBASE:UNIUSD" },
                    { s: "KRAKEN:UNIEUR" },
                    { s: "COINBASE:UNIGBP" },
                    { s: "BINANCE:UNIBTC" },
                    { s: "KRAKEN:UNIETH" },
                    { s: "BINANCE:UNIUSDT" },
                ],
                quick_link: {
                    title: "More Uniswap pairs",
                    href: "/symbols/UNIUSD/markets/",
                },
            },
        ],
        title_link: "/markets/cryptocurrencies/prices-all/",
        width: "100%",
        height: "100%",
        showChart: true,
        showFloatingTooltip: false,
        locale: "en",
        plotLineColorGrowing: "#2962FF",
        plotLineColorFalling: "#2962FF",
        belowLineFillColorGrowing: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorFalling: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorGrowingBottom: "rgba(41, 98, 255, 0)",
        belowLineFillColorFallingBottom: "rgba(41, 98, 255, 0)",
        gridLineColor: "rgba(240, 243, 250, 0)",
        scaleFontColor: "rgba(120, 123, 134, 1)",
        showSymbolLogo: true,
        symbolActiveColor: "rgba(41, 98, 255, 0.12)",
        colorTheme: "light",
    };
    script.innerHTML = JSON.stringify(widgetConfig);

    const widgetContainer = document.getElementById("widgetTwo");
    if (widgetContainer) {
        widgetContainer.appendChild(script);
    }
    script.onload = function() {
        spinnerTwo.style.display = 'none';
    };



    // ======= WIDGET 3 start =======
    const spinnerThree = document.querySelector('.flex-item #spinnerThree');
    spinnerThree.style.display = 'block';

    const script3 = document.createElement('script');
    script3.type = 'text/javascript';
    script3.src = 'https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js';
    script3.async = true;

    const widgetConfig3 = {
        title: "Currencies",
        tabs: [
            {
                title: "Major",
                title_raw: "Major",
                symbols: [
                    { s: "FX_IDC:EURUSD", d: "EUR to USD" },
                    { s: "FX_IDC:USDJPY", d: "USD to JPY" },
                    { s: "FX_IDC:GBPUSD", d: "GBP to USD" },
                    { s: "FX_IDC:AUDUSD", d: "AUD to USD" },
                    { s: "FX_IDC:USDCAD", d: "USD to CAD" },
                    { s: "FX_IDC:USDCHF", d: "USD to CHF" }
                ],
                quick_link: {
                    title: "More majors",
                    href: "/markets/currencies/rates-major/"
                }
            },
            {
                title: "Minor",
                title_raw: "Minor",
                symbols: [
                    { s: "FX_IDC:EURGBP", d: "EUR to GBP" },
                    { s: "FX_IDC:EURJPY", d: "EUR to JPY" },
                    { s: "FX_IDC:GBPJPY", d: "GBP to JPY" },
                    { s: "FX_IDC:CADJPY", d: "CAD to JPY" },
                    { s: "FX_IDC:GBPCAD", d: "GBP to CAD" },
                    { s: "FX_IDC:EURCAD", d: "EUR to CAD" }
                ],
                quick_link: {
                    title: "More minors",
                    href: "/markets/currencies/rates-minor/"
                }
            },
            {
                title: "Exotic",
                title_raw: "Exotic",
                symbols: [
                    { s: "FX_IDC:USDSEK", d: "USD to SEK" },
                    { s: "FX_IDC:USDMXN", d: "USD to MXN" },
                    { s: "FX_IDC:USDZAR", d: "USD to ZAR" },
                    { s: "FX_IDC:EURTRY", d: "EUR to TRY" },
                    { s: "FX_IDC:EURNOK", d: "EUR to NOK" },
                    { s: "FX_IDC:GBPPLN", d: "GBP to PLN" }
                ],
                quick_link: {
                    title: "More exotics",
                    href: "/markets/currencies/rates-exotic/"
                }
            }
        ],
        title_link: "/markets/currencies/rates-major/",
        width: "100%",
        height: "100%",
        showChart: true,
        showFloatingTooltip: false,
        locale: "en",
        plotLineColorGrowing: "#2962FF",
        plotLineColorFalling: "#2962FF",
        belowLineFillColorGrowing: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorFalling: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorGrowingBottom: "rgba(41, 98, 255, 0)",
        belowLineFillColorFallingBottom: "rgba(41, 98, 255, 0)",
        gridLineColor: "rgba(240, 243, 250, 0)",
        scaleFontColor: "rgba(120, 123, 134, 1)",
        showSymbolLogo: true,
        symbolActiveColor: "rgba(41, 98, 255, 0.12)",
        colorTheme: "light"
    };

    script3.innerHTML = JSON.stringify(widgetConfig3);

    const widgetContainer3 = document.getElementById('widgetThree');
    if (widgetContainer3) {
        widgetContainer3.appendChild(script3);
    }
    script3.onload = function() {
        spinnerThree.style.display = 'none';
    };



    // ====== WIDGET 4 start ======
    const spinnerFour = document.querySelector('.flex-item #spinnerFour');
    spinnerFour.style.display = 'block';

    const script4 = document.createElement('script');
    script4.type = 'text/javascript';
    script4.src = 'https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js';
    script4.async = true;

    const widgetConfig4 = {
        title: "Stocks",
        tabs: [
            {
                title: "Financial",
                symbols: [
                    { s: "NYSE:JPM", d: "JPMorgan Chase" },
                    { s: "NYSE:WFC", d: "Wells Fargo Co New" },
                    { s: "NYSE:BAC", d: "Bank Amer Corp" },
                    { s: "NYSE:HSBC", d: "Hsbc Hldgs Plc" },
                    { s: "NYSE:C", d: "Citigroup Inc" },
                    { s: "NYSE:MA", d: "Mastercard Incorporated" }
                ]
            },
            {
                title: "Technology",
                symbols: [
                    { s: "NASDAQ:AAPL", d: "Apple" },
                    { s: "NASDAQ:GOOGL", d: "Alphabet" },
                    { s: "NASDAQ:MSFT", d: "Microsoft" },
                    { s: "NASDAQ:FB", d: "Meta Platforms" },
                    { s: "NYSE:ORCL", d: "Oracle Corp" },
                    { s: "NASDAQ:INTC", d: "Intel Corp" }
                ]
            },
            {
                title: "Services",
                symbols: [
                    { s: "NASDAQ:AMZN", d: "Amazon" },
                    { s: "NYSE:BABA", d: "Alibaba Group Hldg Ltd" },
                    { s: "NYSE:T", d: "At&t Inc" },
                    { s: "NYSE:WMT", d: "Walmart" },
                    { s: "NYSE:V", d: "Visa" }
                ]
            }
        ],
        width: "100%",
        height: "100%",
        showChart: true,
        showFloatingTooltip: false,
        locale: "en",
        plotLineColorGrowing: "#2962FF",
        plotLineColorFalling: "#2962FF",
        belowLineFillColorGrowing: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorFalling: "rgba(41, 98, 255, 0.12)",
        belowLineFillColorGrowingBottom: "rgba(41, 98, 255, 0)",
        belowLineFillColorFallingBottom: "rgba(41, 98, 255, 0)",
        gridLineColor: "rgba(240, 243, 250, 0)",
        scaleFontColor: "rgba(120, 123, 134, 1)",
        showSymbolLogo: true,
        symbolActiveColor: "rgba(41, 98, 255, 0.12)",
        colorTheme: "light"
    };

    script4.innerHTML = JSON.stringify(widgetConfig4);

    const widgetContainer4 = document.getElementById('widgetFour');
    if (widgetContainer4) {
        widgetContainer4.appendChild(script4);
    }

    script4.onload = function() {
        spinnerFour.style.display = 'none';
    };
};

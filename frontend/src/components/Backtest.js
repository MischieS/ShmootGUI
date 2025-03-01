import React, { useState } from "react";
import axios from "axios";

function Backtest() {
    const [results, setResults] = useState(null);

    const runBacktest = async () => {
        const response = await axios.get("http://localhost:8000/api/backtest/BTCUSDT_1m");
        setResults(response.data);
    };

    return (
        <div>
            <h2>Backtesting</h2>
            <button onClick={runBacktest}>Run Backtest</button>

            {results && (
                <div>
                    <h3>Results:</h3>
                    <p>Total Profit: ${results.total_profit.toFixed(2)}</p>
                    <p>Win Rate: {results.win_rate.toFixed(2)}%</p>
                    <p>Max Drawdown: {results.max_drawdown.toFixed(2)}%</p>
                </div>
            )}
        </div>
    );
}

export default Backtest;

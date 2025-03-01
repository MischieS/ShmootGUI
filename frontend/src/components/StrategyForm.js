import React, { useState } from "react";
import axios from "axios";

function StrategyForm() {
    const [settings, setSettings] = useState({
        ema_periods: [5, 10, 20],
        rsi_period: 14,
        macd_fast: 12,
        macd_slow: 26,
        macd_signal: 9,
        bollinger_period: 20
    });

    const handleChange = (e) => {
        setSettings({ ...settings, [e.target.name]: Number(e.target.value) });
    };

    const handleSubmit = async () => {
        await axios.post("http://localhost:8000/api/update-strategy-config", settings);
        alert("Strategy settings updated!");
    };

    return (
        <div>
            <h2>Configure Strategy</h2>
            <label>EMA Periods: </label>
            <input type="text" name="ema_periods" 
                value={settings.ema_periods.join(",")} 
                onChange={(e) => setSettings({ ...settings, ema_periods: e.target.value.split(",").map(Number) })}
            />
            
            <label>RSI Period: </label>
            <input type="number" name="rsi_period" value={settings.rsi_period} onChange={handleChange} />

            <button onClick={handleSubmit}>Save Settings</button>
        </div>
    );
}

export default StrategyForm;

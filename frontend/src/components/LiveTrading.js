import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

function LiveTrading() {
    const [marketData, setMarketData] = useState([]);
    
    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8000/ws/live/BTCUSDT_1m");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMarketData((prev) => [...prev.slice(-20), data]); // Keep last 20 points
        };

        return () => socket.close();
    }, []);

    return (
        <div>
            <h2>Live Market Data</h2>
            <LineChart width={600} height={300} data={marketData}>
                <XAxis dataKey="timestamp" />
                <YAxis />
                <CartesianGrid stroke="#eee" />
                <Tooltip />
                <Line type="monotone" dataKey="close" stroke="#8884d8" />
            </LineChart>
        </div>
    );
}

export default LiveTrading;

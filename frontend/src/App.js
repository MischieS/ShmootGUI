import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LiveTrading from "./components/LiveTrading";
import Backtest from "./components/Backtest";
import StrategyForm from "./components/StrategyForm";
import Navbar from "./components/Navbar";

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<LiveTrading />} />
                <Route path="/backtest" element={<Backtest />} />
                <Route path="/strategy" element={<StrategyForm />} />
            </Routes>
        </Router>
    );
}

export default App;

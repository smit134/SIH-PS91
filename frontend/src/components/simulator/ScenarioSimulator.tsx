"use client";

import React, { useState } from 'react';

export function ScenarioSimulator() {
  const [salesVolume, setSalesVolume] = useState<number>(100);
  const [sellingPrice, setSellingPrice] = useState<number>(500);
  const [rawMaterialCost, setRawMaterialCost] = useState<number>(200);
  const [labourCost, setLabourCost] = useState<number>(15000);
  const [loanAmount, setLoanAmount] = useState<number>(100000);
  const [interestRate, setInterestRate] = useState<number>(10);
  const [tenureMonths, setTenureMonths] = useState<number>(36);

  // Calculations
  const monthlyRevenue = salesVolume * sellingPrice;
  const monthlyMaterialCost = salesVolume * rawMaterialCost;
  
  // EMI Calculation: P * r * (1+r)^n / ((1+r)^n - 1)
  const monthlyInterestRate = (interestRate / 100) / 12;
  const emi = loanAmount > 0 && tenureMonths > 0 && monthlyInterestRate > 0
    ? (loanAmount * monthlyInterestRate * Math.pow(1 + monthlyInterestRate, tenureMonths)) / (Math.pow(1 + monthlyInterestRate, tenureMonths) - 1)
    : 0;

  const totalMonthlyCost = monthlyMaterialCost + labourCost + emi;
  const monthlyProfit = monthlyRevenue - totalMonthlyCost;
  
  const totalProjectCost = 200000; // Fixed for simulation simplicity
  const breakEvenMonths = monthlyProfit > 0 ? Math.ceil(totalProjectCost / monthlyProfit) : 'Never';
  
  const riskLevel = monthlyProfit < 5000 ? 'High' : (monthlyProfit < 15000 ? 'Medium' : 'Low');

  return (
    <div className="w-full bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex flex-col md:flex-row gap-8">
      {/* Inputs Section */}
      <div className="flex-1 space-y-6">
        <h3 className="text-xl font-bold text-slate-800">Business Scenario Simulator</h3>
        <p className="text-sm text-slate-500">Adjust the sliders to see how changes affect your profitability.</p>
        
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-1 text-sm font-medium text-slate-700">
              <label>Monthly Sales (units)</label>
              <span>{salesVolume}</span>
            </div>
            <input type="range" min="10" max="500" value={salesVolume} onChange={(e) => setSalesVolume(Number(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600" />
          </div>
          
          <div>
            <div className="flex justify-between mb-1 text-sm font-medium text-slate-700">
              <label>Selling Price (₹)</label>
              <span>₹{sellingPrice}</span>
            </div>
            <input type="range" min="100" max="2000" step="50" value={sellingPrice} onChange={(e) => setSellingPrice(Number(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600" />
          </div>

          <div>
            <div className="flex justify-between mb-1 text-sm font-medium text-slate-700">
              <label>Raw Material Cost (₹/unit)</label>
              <span>₹{rawMaterialCost}</span>
            </div>
            <input type="range" min="50" max="1000" step="10" value={rawMaterialCost} onChange={(e) => setRawMaterialCost(Number(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600" />
          </div>

          <div>
            <div className="flex justify-between mb-1 text-sm font-medium text-slate-700">
              <label>Loan Amount (₹)</label>
              <span>₹{loanAmount.toLocaleString()}</span>
            </div>
            <input type="range" min="0" max="500000" step="10000" value={loanAmount} onChange={(e) => setLoanAmount(Number(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600" />
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="flex-1 bg-slate-50 rounded-xl p-6 border border-slate-100 flex flex-col justify-center">
        <h4 className="text-sm font-bold tracking-wider text-slate-500 uppercase mb-6">Simulation Results</h4>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-100">
            <p className="text-xs text-slate-500 mb-1">Monthly Revenue</p>
            <p className="text-xl font-bold text-slate-800">₹{monthlyRevenue.toLocaleString()}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-100">
            <p className="text-xs text-slate-500 mb-1">Monthly Cost</p>
            <p className="text-xl font-bold text-slate-800">₹{Math.round(totalMonthlyCost).toLocaleString()}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-100">
            <p className="text-xs text-slate-500 mb-1">Estimated Profit</p>
            <p className={`text-2xl font-bold ${monthlyProfit > 0 ? 'text-teal-600' : 'text-red-500'}`}>
              ₹{Math.round(monthlyProfit).toLocaleString()}
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-100">
            <p className="text-xs text-slate-500 mb-1">Monthly EMI</p>
            <p className="text-xl font-bold text-amber-600">₹{Math.round(emi).toLocaleString()}</p>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-200">
          <div>
            <p className="text-sm text-slate-500">Break-even</p>
            <p className="font-semibold text-slate-800">{breakEvenMonths} {breakEvenMonths !== 'Never' && 'months'}</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-slate-500">Risk Level</p>
            <p className={`font-bold ${riskLevel === 'Low' ? 'text-teal-600' : (riskLevel === 'Medium' ? 'text-amber-500' : 'text-red-500')}`}>
              {riskLevel}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

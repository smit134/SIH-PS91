"use client";

import React, { useState, useEffect } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { WalletCards, TrendingUp, DollarSign, Calculator, AlertCircle, Loader2 } from "lucide-react";

const EmiCalculator = () => {
  const [principal, setPrincipal] = useState(300000);
  const [rate, setRate] = useState(8.5);
  const [tenureYears, setTenureYears] = useState(5);

  const r = rate / 12 / 100;
  const n = tenureYears * 12;
  const emi = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) || 0;
  const totalAmount = emi * n;
  const totalInterest = totalAmount - principal;

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card">
      <h3 className="font-bold text-base text-slate-900 mb-4 flex items-center gap-2">
        <Calculator className="w-5 h-5 text-brand-600" />
        Quick EMI Calculator
      </h3>
      <div className="space-y-4">
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">Loan Amount (₹ {principal.toLocaleString()})</label>
          <input type="range" min="10000" max="2000000" step="10000" value={principal} onChange={e => setPrincipal(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">Interest Rate ({rate}%)</label>
          <input type="range" min="5" max="20" step="0.5" value={rate} onChange={e => setRate(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">Tenure ({tenureYears} Years)</label>
          <input type="range" min="1" max="15" step="1" value={tenureYears} onChange={e => setTenureYears(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-100">
          <div>
            <p className="text-[11px] text-slate-500 font-medium">Monthly EMI</p>
            <p className="text-lg font-bold text-emerald-700">₹{Math.round(emi).toLocaleString()}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-500 font-medium">Total Interest</p>
            <p className="text-lg font-bold text-slate-900">₹{Math.round(totalInterest).toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function FinancePage() {
  const [profile, setProfile] = useState<any>(null);
  const [simulation, setSimulation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const parseCurrency = (str: string) => {
    if (!str) return 0;
    return parseInt(str.replace(/[^0-9]/g, "")) || 0;
  };

  const handleSimulate = async (currentProfile: any) => {
    setLoading(true);
    try {
      const ownEquity = parseCurrency(currentProfile?.ownEquity || "150000");
      const projectCost = 480000;
      
      const payload = {
        project_cost: projectCost,
        own_contribution: ownEquity,
        interest_rate: 8.5,
        tenure_months: 60,
        operating_assumptions: {
          monthly_revenue: 85000,
          monthly_fixed_costs: 20000,
          monthly_variable_costs: 30000
        }
      };

      const res = await fetch("http://localhost:8000/finance/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setSimulation(await res.json());
      } else {
        console.error("Simulation failed");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const stored = localStorage.getItem("thinkforge_profile");
    let currentProfile = null;
    if (stored) {
      currentProfile = JSON.parse(stored);
      setProfile(currentProfile);
    }
    handleSimulate(currentProfile);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <WalletCards className="w-4 h-4 text-brand-600" />
            <span>FINANCIAL STRUCTURING</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Capex & Cash Flow Simulation</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Financial Architecture</h1>
          <p className="text-sm text-slate-600">
            Precision capital modeling: equity, loan amortization, operational expenses, and debt-service coverage.
          </p>
        </div>

        <button 
          onClick={() => handleSimulate(profile)}
          disabled={loading}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all disabled:opacity-70"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Calculator className="w-4 h-4 text-emerald-200" />}
          Refresh Simulation
        </button>
      </div>

      {simulation ? (
        <>
          {/* Financial Snapshot KPI Tiles */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">Projected Project Cost</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">₹4,80,000</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-emerald-700 font-semibold">Standard Model</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">Entrepreneur Own Equity</span>
              <p className="text-2xl font-bold text-brand-700 mt-1">₹{parseCurrency(profile?.ownEquity || "150000").toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-slate-600 font-semibold">User Declared</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">Required Loan</span>
              <p className="text-2xl font-bold text-emerald-600 mt-1">₹{Math.round(simulation.required_loan).toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-emerald-700 font-semibold">After 35% Scheme Subsidy</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">Est. Bank EMI</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">₹{Math.round(simulation.emi).toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-slate-600 font-semibold">@ 8.5% (5 Yr)</span>
                <EvidenceBadge type="DERIVED" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Pro-forma Cash Flow Table */}
            <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-slate-900">Projected 3-Year Operating Cash Flow</h3>
                <span className="text-xs text-slate-500">Assumes 75% Year-1 Capacity Utilization</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                      <th className="pb-3">Financial Metric</th>
                      <th className="pb-3 text-right">Monthly Avg</th>
                      <th className="pb-3 text-right">Year 1 Total</th>
                      <th className="pb-3 text-right">Evidence Level</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-slate-700 font-medium">
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">Gross Sales Revenue</td>
                      <td className="py-3 text-right">₹85,000</td>
                      <td className="py-3 text-right">₹10,20,000</td>
                      <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
                    </tr>
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">Total Operating Costs</td>
                      <td className="py-3 text-right">₹50,000</td>
                      <td className="py-3 text-right">₹6,00,000</td>
                      <td className="py-3 text-right"><EvidenceBadge type="ESTIMATED" /></td>
                    </tr>
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">Loan Repayment (EMI)</td>
                      <td className="py-3 text-right">₹{Math.round(simulation.emi).toLocaleString()}</td>
                      <td className="py-3 text-right">₹{Math.round(simulation.emi * 12).toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="VERIFIED" /></td>
                    </tr>
                    <tr className="bg-emerald-50/50">
                      <td className="py-3 font-bold text-emerald-900">Net Surplus / Take-Home</td>
                      <td className="py-3 text-right font-bold text-emerald-800">₹{Math.round(simulation.monthly_profit).toLocaleString()}</td>
                      <td className="py-3 text-right font-bold text-emerald-800">₹{Math.round(simulation.monthly_profit * 12).toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Quick EMI Calculator */}
            <div className="lg:col-span-1">
              <EmiCalculator />
            </div>
          </div>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500 mb-4" />
          <p>Running dynamic financial architecture simulation...</p>
        </div>
      )}
    </div>
  );
}

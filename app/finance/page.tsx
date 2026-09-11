import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { WalletCards, TrendingUp, DollarSign, Calculator, AlertCircle } from "lucide-react";

export default function FinancePage() {
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

        <button className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all">
          <Calculator className="w-4 h-4 text-emerald-200" />
          Run Amortization Simulation
        </button>
      </div>

      {/* Financial Snapshot KPI Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
          <span className="text-xs font-medium text-slate-500">Projected Project Cost</span>
          <p className="text-2xl font-bold text-slate-900 mt-1">₹4,80,000</p>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-emerald-700 font-semibold">Capex + 3 Mo Working Cap</span>
            <EvidenceBadge type="DERIVED" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
          <span className="text-xs font-medium text-slate-500">Entrepreneur Own Equity</span>
          <p className="text-2xl font-bold text-brand-700 mt-1">₹1,50,000</p>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-600 font-semibold">31.2% Equity Ratio</span>
            <EvidenceBadge type="VERIFIED" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
          <span className="text-xs font-medium text-slate-500">Scheme Credit Subsidy</span>
          <p className="text-2xl font-bold text-emerald-600 mt-1">₹1,68,000</p>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-emerald-700 font-semibold">PMEGP 35% Rural MoSJE</span>
            <EvidenceBadge type="VERIFIED" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
          <span className="text-xs font-medium text-slate-500">Est. Bank Loan / EMI</span>
          <p className="text-2xl font-bold text-slate-900 mt-1">₹1,62,000</p>
          <div className="mt-2 flex items-center justify-between text-xs">
            <span className="text-slate-600 font-semibold">₹3,420/mo @ 8.5% (5 Yr)</span>
            <EvidenceBadge type="DERIVED" />
          </div>
        </div>
      </div>

      {/* Pro-forma Cash Flow Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-base text-slate-900">Projected 3-Year Operating Cash Flow</h3>
          <span className="text-xs text-slate-500">Assumes 75% Year-1 Capacity Utilization</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="pb-3">Financial Metric</th>
                <th className="pb-3 text-right">Year 1</th>
                <th className="pb-3 text-right">Year 2</th>
                <th className="pb-3 text-right">Year 3</th>
                <th className="pb-3 text-right">Evidence Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700 font-medium">
              <tr>
                <td className="py-3 font-semibold text-slate-900">Gross Sales Revenue</td>
                <td className="py-3 text-right">₹6,40,000</td>
                <td className="py-3 text-right">₹9,80,000</td>
                <td className="py-3 text-right">₹13,20,000</td>
                <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
              </tr>
              <tr>
                <td className="py-3 font-semibold text-slate-900">Direct Operating Costs</td>
                <td className="py-3 text-right">₹3,80,000</td>
                <td className="py-3 text-right">₹5,40,000</td>
                <td className="py-3 text-right">₹7,10,000</td>
                <td className="py-3 text-right"><EvidenceBadge type="ESTIMATED" /></td>
              </tr>
              <tr>
                <td className="py-3 font-semibold text-slate-900">Loan Repayment (P + I)</td>
                <td className="py-3 text-right">₹41,040</td>
                <td className="py-3 text-right">₹41,040</td>
                <td className="py-3 text-right">₹41,040</td>
                <td className="py-3 text-right"><EvidenceBadge type="VERIFIED" /></td>
              </tr>
              <tr className="bg-emerald-50/50">
                <td className="py-3 font-bold text-emerald-900">Net Surplus / Take-Home</td>
                <td className="py-3 text-right font-bold text-emerald-800">₹2,18,960</td>
                <td className="py-3 text-right font-bold text-emerald-800">₹3,98,960</td>
                <td className="py-3 text-right font-bold text-emerald-800">₹5,68,960</td>
                <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

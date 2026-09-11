import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { MapPinned, Store, TrendingUp, AlertTriangle } from "lucide-react";

export default function LocalInsightsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <MapPinned className="w-4 h-4 text-brand-600" />
            <span>HYPER-LOCAL GEOGRAPHIC INTELLIGENCE</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Wardha APMC Catchment</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Local Market Intelligence</h1>
          <p className="text-sm text-slate-600">
            District economic indicators, competitor density heatmap, mandi throughput, and logistical bottlenecks.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Visual Map Area */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-card flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 className="font-bold text-base text-slate-900">District Geospatial Demand Index</h3>
            <EvidenceBadge type="VERIFIED" />
          </div>

          <div className="my-5 aspect-[16/10] bg-slate-900 rounded-xl p-6 relative overflow-hidden flex flex-col justify-between text-white">
            <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#2dd4bf_1px,transparent_1px)] [background-size:16px_16px]" />
            <div className="relative z-10 flex items-center justify-between text-xs">
              <span className="bg-slate-800/90 px-3 py-1 rounded-full border border-slate-700 font-mono">
                Wardha Cluster • Lat 20.7453° N, 78.6022° E
              </span>
              <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full font-semibold">
                High Agro Density
              </span>
            </div>

            <div className="relative z-10 text-center space-y-2 my-auto">
              <div className="w-16 h-16 rounded-full bg-brand-500/20 border-2 border-brand-400 flex items-center justify-center mx-auto shadow-glow-teal animate-pulse">
                <MapPinned className="w-8 h-8 text-emerald-300" />
              </div>
              <h4 className="text-lg font-bold text-white">Wardha Central Micro-Region</h4>
              <p className="text-xs text-slate-300 max-w-md mx-auto">
                Mandi Radius: 18km • 42 Cultivation Clusters • High unmet demand for post-harvest pre-sorting.
              </p>
            </div>

            <div className="relative z-10 grid grid-cols-3 gap-2 text-center text-xs pt-3 border-t border-slate-800">
              <div>
                <p className="text-slate-400 text-[10px]">APMC Mandi Arrival</p>
                <p className="font-bold text-white">1,420 Quintals/Day</p>
              </div>
              <div>
                <p className="text-slate-400 text-[10px]">Active Competitors</p>
                <p className="font-bold text-amber-400">Low (2 Units in 25km)</p>
              </div>
              <div>
                <p className="text-slate-400 text-[10px]">Power Reliability</p>
                <p className="font-bold text-emerald-400">18.5 Hrs/Day (3-Phase)</p>
              </div>
            </div>
          </div>
        </div>

        {/* District Local Stats */}
        <div className="space-y-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <Store className="w-4 h-4 text-brand-600" />
              <span>Competitor Saturation</span>
            </div>
            <p className="text-2xl font-bold text-slate-900">18% Saturation</p>
            <p className="text-xs text-emerald-700 font-semibold mt-1">
              Underserved Niche: Premium grading & solar packaging
            </p>
            <div className="mt-3 pt-3 border-t border-slate-100">
              <EvidenceBadge type="DERIVED" />
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <TrendingUp className="w-4 h-4 text-emerald-600" />
              <span>Seasonal Price Premium</span>
            </div>
            <p className="text-2xl font-bold text-emerald-700">+22.4% Off-Season</p>
            <p className="text-xs text-slate-600 mt-1">
              Storage can fetch up to ₹450/quintal price lift in Oct-Dec.
            </p>
            <div className="mt-3 pt-3 border-t border-slate-100">
              <EvidenceBadge type="VERIFIED" />
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span>Key Risk Factor</span>
            </div>
            <p className="text-sm font-bold text-slate-900">Logistics Transport Scarcity</p>
            <p className="text-xs text-slate-600 mt-1">
              Peak harvest weeks experience truck shortage; partner with Wardha FPO recommended.
            </p>
            <div className="mt-3 pt-3 border-t border-slate-100">
              <EvidenceBadge type="ESTIMATED" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

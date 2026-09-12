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

          <div className="my-5 aspect-[16/10] bg-slate-200 rounded-xl relative overflow-hidden flex flex-col shadow-inner">
            <iframe 
              width="100%" 
              height="100%" 
              src="https://maps.google.com/maps?q=20.7453,78.6022&z=11&output=embed" 
              frameBorder="0" 
              style={{ border: 0, position: 'absolute', inset: 0 }} 
              allowFullScreen 
              title="Local Area Map"
            />
            
            {/* Overlay Elements */}
            <div className="relative z-10 flex items-center justify-between p-4 pointer-events-none">
              <span className="bg-slate-900/90 text-white px-3 py-1.5 rounded-full border border-slate-700 font-mono text-xs shadow-lg backdrop-blur-sm">
                Wardha Cluster • Lat 20.7453° N, 78.6022° E
              </span>
              <span className="bg-emerald-500/90 text-white border border-emerald-400 px-3 py-1.5 rounded-full font-bold text-xs shadow-lg backdrop-blur-sm">
                High Agro Density
              </span>
            </div>

            <div className="mt-auto relative z-10 grid grid-cols-3 gap-2 text-center text-xs p-4 bg-slate-900/90 backdrop-blur-md text-white border-t border-slate-800 pointer-events-none">
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

import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { Compass, Sparkles, Filter, ArrowUpRight } from "lucide-react";
import Link from "next/link";

export default function OpportunitiesPage() {
  const opportunities = [
    {
      title: "Solar-Powered Cold-Chain Sorting Unit",
      sector: "Agri-Tech & Post-Harvest",
      viabilityScore: 89,
      capitalNeeded: "₹4.8 Lakhs",
      ownEquity: "₹1.2 Lakhs",
      payback: "14 months",
      roi: "28.5%",
      evidence: "VERIFIED" as const,
      subsidy: "PMEGP 35% Credit Subsidy Eligible",
    },
    {
      title: "Bio-Waste Pelletization & Briquette Plant",
      sector: "Renewable Energy & Biomass",
      viabilityScore: 83,
      capitalNeeded: "₹6.5 Lakhs",
      ownEquity: "₹1.5 Lakhs",
      payback: "18 months",
      roi: "24.0%",
      evidence: "DERIVED" as const,
      subsidy: "SATAT / MSME Cluster Grant",
    },
    {
      title: "Cotton-Stalk Fiber Extraction Micro-Unit",
      sector: "Agro-Textile Secondary Material",
      viabilityScore: 78,
      capitalNeeded: "₹3.2 Lakhs",
      ownEquity: "₹80,000",
      payback: "11 months",
      roi: "31.2%",
      evidence: "DERIVED" as const,
      subsidy: "KVIC Special Component",
    },
    {
      title: "Dairy Value-Add: Paneer & Whey Processing",
      sector: "Livestock & Dairy",
      viabilityScore: 74,
      capitalNeeded: "₹2.9 Lakhs",
      ownEquity: "₹75,000",
      payback: "9 months",
      roi: "34.0%",
      evidence: "ESTIMATED" as const,
      subsidy: "National Dairy Plan Micro-Grant",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <Compass className="w-4 h-4 text-brand-600" />
            <span>OPPORTUNITY ENGINE</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Wardha Cluster Analysis</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Recommended Opportunities</h1>
          <p className="text-sm text-slate-600">
            Feasibility-matched rural enterprise models ranked by capital fit, local demand, and evidence reliability.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-sm">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            Filter by Capital
          </button>
          <Link
            href="/register"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-200" />
            Adjust Capabilities
          </Link>
        </div>
      </div>

      {/* Grid of Opportunities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {opportunities.map((opp) => (
          <div
            key={opp.title}
            className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-card hover:shadow-card-elevated hover:border-brand-500/50 transition-all group"
          >
            <div className="flex items-start justify-between gap-2 mb-3">
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                {opp.sector}
              </span>
              <EvidenceBadge type={opp.evidence} />
            </div>

            <h3 className="text-lg font-bold text-slate-900 group-hover:text-brand-700 transition-colors">
              {opp.title}
            </h3>

            <div className="mt-4 grid grid-cols-3 gap-3 py-3 px-3.5 rounded-xl bg-slate-50 border border-slate-100 text-center">
              <div>
                <p className="text-[11px] text-slate-500 font-medium">Capex Needed</p>
                <p className="text-sm font-bold text-slate-900 mt-0.5">{opp.capitalNeeded}</p>
              </div>
              <div>
                <p className="text-[11px] text-slate-500 font-medium">Payback Period</p>
                <p className="text-sm font-bold text-brand-700 mt-0.5">{opp.payback}</p>
              </div>
              <div>
                <p className="text-[11px] text-slate-500 font-medium">Expected ROI</p>
                <p className="text-sm font-bold text-emerald-600 mt-0.5">{opp.roi}</p>
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between pt-3 border-t border-slate-100">
              <div className="flex items-center gap-1.5 text-xs text-slate-600">
                <span className="w-2 h-2 rounded-full bg-brand-500" />
                <span>{opp.subsidy}</span>
              </div>
              <div className="flex items-center gap-1 text-xs font-bold text-brand-700 group-hover:translate-x-0.5 transition-transform">
                <span>Evaluate</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

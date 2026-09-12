"use client";

import React, { useState, useEffect } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { Compass, Sparkles, Filter, ArrowUpRight, Loader2, CheckCircle2, AlertTriangle, X } from "lucide-react";
import Link from "next/link";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOpp, setSelectedOpp] = useState<any | null>(null);

  useEffect(() => {
    const fetchOpps = async () => {
      try {
        const storedProfile = localStorage.getItem("thinkforge_profile");
        const rawProfile = storedProfile ? JSON.parse(storedProfile) : {};
        
        // Map UI profile format to Backend EntrepreneurProfile schema
        const profile = {
          user_id: "demo_user",
          name: "Rural Entrepreneur",
          available_capital: rawProfile.ownEquity ? parseInt(rawProfile.ownEquity.replace(/[^0-9]/g, "")) : 150000,
          skills: [rawProfile.primarySkill || "Agri-Processing"],
          experience_years: 2.0,
          resources: [rawProfile.landAccess || "Owned", rawProfile.powerSupply || "3-Phase"],
          interests: [rawProfile.sectorInterest || "Post-Harvest"],
          location: {
            latitude: 20.7453,
            longitude: 78.6022,
            village_or_town: rawProfile.block || "Deoli",
            district: rawProfile.district || "Wardha",
            state: rawProfile.state || "Maharashtra",
            service_radius_km: 15.0
          },
          risk_preference: "Medium",
          has_transport_access: !!rawProfile.transportVehicle,
          has_market_connections: false,
          has_digital_tools: true
        };

        const res = await fetch("http://localhost:8000/api/intelligence/opportunity/recommendations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(profile)
        });

        if (res.ok) {
          const data = await res.json();
          setOpportunities(data);
        } else {
          console.error("Failed to fetch opportunities", await res.text());
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchOpps();
  }, []);

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
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500 mb-4" />
          <p>Analyzing rural market feasibility...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {opportunities.map((opp, idx) => {
            return (
              <div
                key={idx}
                className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-card hover:shadow-card-elevated hover:border-brand-500/50 transition-all group flex flex-col"
              >
                <div className="flex items-start justify-between gap-2 mb-3">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {opp.sector || "Agri-Tech & Post-Harvest"}
                  </span>
                  <EvidenceBadge type={opp.evidence_class || "VERIFIED"} />
                </div>

                <h3 className="text-lg font-bold text-slate-900 group-hover:text-brand-700 transition-colors">
                  {opp.business_name || opp.title}
                </h3>

                <div className="mt-4 grid grid-cols-3 gap-3 py-3 px-3.5 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div>
                    <p className="text-[11px] text-slate-500 font-medium">Capex Needed</p>
                    <p className="text-sm font-bold text-slate-900 mt-0.5">
                      ₹{(opp.capital_required_rec || opp.capitalNeeded || 0).toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-[11px] text-slate-500 font-medium">Payback</p>
                    <p className="text-sm font-bold text-brand-700 mt-0.5">
                      {opp.estimated_break_even_months || opp.payback || 12} mo
                    </p>
                  </div>
                  <div>
                    <p className="text-[11px] text-slate-500 font-medium">Fit Score</p>
                    <p className="text-sm font-bold text-emerald-600 mt-0.5">
                      {Math.round(opp.overall_fit_score || opp.viabilityScore || 0)}%
                    </p>
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between pt-3 border-t border-slate-100">
                  <div className="flex items-center gap-1.5 text-xs text-slate-600">
                    <span className="w-2 h-2 rounded-full bg-brand-500" />
                    <span>Eligible for Credit Subsidy</span>
                  </div>
                  <button
                    onClick={() => setSelectedOpp(opp)}
                    className="flex items-center gap-1 text-xs font-bold text-brand-700 hover:text-brand-800 group-hover:translate-x-0.5 transition-transform"
                  >
                    <span>Evaluate Details</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal Overlay */}
      {selectedOpp && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/50 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between p-5 border-b border-slate-100">
              <div>
                <span className="text-[11px] font-semibold text-brand-600 uppercase tracking-wider mb-1 block">
                  Detailed Evaluation
                </span>
                <h3 className="text-lg font-bold text-slate-900 leading-tight">
                  {selectedOpp.business_name || selectedOpp.title}
                </h3>
              </div>
              <button 
                onClick={() => setSelectedOpp(null)}
                className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 space-y-6 max-h-[60vh] overflow-y-auto">
              <div>
                <h4 className="text-xs font-bold text-slate-800 mb-3 uppercase tracking-wider">Why Recommended</h4>
                <ul className="space-y-2">
                  {selectedOpp.why_recommended?.map((reason: string, i: number) => (
                    <li key={i} className="flex items-start gap-2.5 text-sm text-slate-600">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              {selectedOpp.why_not_perfect && selectedOpp.why_not_perfect.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-slate-800 mb-3 uppercase tracking-wider">Considerations & Risks</h4>
                  <ul className="space-y-2">
                    {selectedOpp.why_not_perfect.map((reason: string, i: number) => (
                      <li key={i} className="flex items-start gap-2.5 text-sm text-slate-600">
                        <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                        <span>{reason}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="p-5 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
              <button 
                onClick={() => setSelectedOpp(null)}
                className="px-5 py-2.5 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
              >
                Close
              </button>
              <Link 
                href="/finance" 
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-600 text-white text-sm font-bold hover:bg-brand-700 shadow-glow-teal transition-all"
              >
                <span>Run Financial Simulation</span>
                <ArrowUpRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

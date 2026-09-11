import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { Users2, MapPin, Handshake, ShieldCheck, PhoneCall } from "lucide-react";

export default function PartnersPage() {
  const partners = [
    {
      name: "Wardha Farmer Producer Co. (FPO)",
      type: "Aggregator / Raw Material Supply",
      location: "Deoli Taluka (14 km away)",
      members: "340 Active Farmers",
      complementaryFit: "Raw Orange & Cotton Biomass Supply",
      evidence: "VERIFIED" as const,
      trustScore: "96%",
    },
    {
      name: "Vidarbha Agro Logistics & Cold Storage",
      type: "Infrastructure & Cold Chain",
      location: "MIDC Wardha (8 km away)",
      members: "200 MT Chilling Capacity",
      complementaryFit: "Shared Refrigeration & Last-Mile Dispatch",
      evidence: "VERIFIED" as const,
      trustScore: "91%",
    },
    {
      name: "Mahila Krishi SHG Cluster (12 Units)",
      type: "Production & Packaging Partner",
      location: "Seloo Block (19 km away)",
      members: "85 Skilled Artisans",
      complementaryFit: "Sorting, Grading & Manual Packaging",
      evidence: "DERIVED" as const,
      trustScore: "88%",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <Users2 className="w-4 h-4 text-brand-600" />
            <span>PARTNER ECOSYSTEM</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Capability Complementarity</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Matched Local Partners</h1>
          <p className="text-sm text-slate-600">
            Discover verified FPOs, SHGs, and logistics providers that bridge your equipment, space, or market access gaps.
          </p>
        </div>

        <button className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all">
          <Handshake className="w-4 h-4 text-emerald-200" />
          Request Partner Introduction
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {partners.map((partner) => (
          <div
            key={partner.name}
            className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card hover:shadow-card-elevated transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <EvidenceBadge type={partner.evidence} />
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                  Trust {partner.trustScore}
                </span>
              </div>

              <h3 className="font-bold text-base text-slate-900 mt-2">{partner.name}</h3>
              <p className="text-xs font-semibold text-brand-700 mt-0.5">{partner.type}</p>

              <div className="mt-3 space-y-1.5 text-xs text-slate-600">
                <div className="flex items-center gap-1.5 text-slate-500">
                  <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>{partner.location}</span>
                </div>
                <div className="flex items-center gap-1.5 text-slate-500">
                  <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>{partner.members}</span>
                </div>
              </div>

              <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  Capability Synergy
                </p>
                <p className="text-xs text-slate-700 mt-1 font-medium leading-relaxed">
                  {partner.complementaryFit}
                </p>
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[11px] text-slate-400 font-medium">Verified by District MSME</span>
              <button className="inline-flex items-center gap-1 text-xs font-bold text-brand-700 hover:text-brand-800">
                <PhoneCall className="w-3.5 h-3.5" />
                Connect
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

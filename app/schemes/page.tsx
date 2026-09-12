import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { Landmark, CheckCircle, ExternalLink, Sparkles } from "lucide-react";

export default function SchemesPage() {
  const schemes = [
    {
      title: "PMEGP (Prime Minister's Employment Generation Programme)",
      nodalAgency: "KVIC / Ministry of MSME",
      eligibilityMatch: "95% Match",
      subsidyRate: "35% Rural Subsidy",
      maxProjectCost: "₹50 Lakhs (Manufacturing)",
      evidence: "VERIFIED" as const,
      status: "Eligible for Instant Application",
      description: "Credit-linked subsidy scheme offering 35% margin money assistance for rural micro-enterprises under MoSJE priority category.",
      url: "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
    },
    {
      title: "PMFME (PM Formalisation of Micro Food Processing Enterprises)",
      nodalAgency: "Ministry of Food Processing Industries (MoFPI)",
      eligibilityMatch: "91% Match",
      subsidyRate: "35% Credit-Linked Grant (Max ₹10L)",
      maxProjectCost: "₹30 Lakhs",
      evidence: "VERIFIED" as const,
      status: "Cluster Aligned (Wardha Citrus & Pulses)",
      description: "Provides financial, technical, and business support for the upgradation of existing and new micro-food processing units.",
      url: "https://pmfme.mofpi.gov.in/",
    },
    {
      title: "Venture Capital Fund for Scheduled Castes / OBCs (VCF-SC/BC)",
      nodalAgency: "IFCI / Ministry of Social Justice & Empowerment",
      eligibilityMatch: "86% Match",
      subsidyRate: "Concessional Equity & Low-Interest Debt",
      maxProjectCost: "Up to ₹15 Crores",
      evidence: "VERIFIED" as const,
      status: "MoSJE Direct Channel",
      description: "Concessional financing and incubation support for first-generation marginalized rural innovators and micro-manufacturers.",
      url: "https://vcfsc.in/",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <Landmark className="w-4 h-4 text-brand-600" />
            <span>POLICY & SUBSIDY ROUTING</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Government Scheme Matching</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Matched Government Schemes</h1>
          <p className="text-sm text-slate-600">
            Auto-matched Central and State subsidy programs tailored to your caste category, rural location, and capital scale.
          </p>
        </div>

        <button className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all">
          <Sparkles className="w-4 h-4 text-emerald-200" />
          Auto-Fill Scheme Application
        </button>
      </div>

      <div className="space-y-4">
        {schemes.map((scheme) => (
          <div
            key={scheme.title}
            className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card hover:border-brand-500/60 transition-all"
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    {scheme.nodalAgency}
                  </span>
                  <EvidenceBadge type={scheme.evidence} />
                </div>
                <h3 className="text-lg font-bold text-slate-900">{scheme.title}</h3>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                  {scheme.eligibilityMatch}
                </span>
                <a 
                  href={scheme.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-900 text-white hover:bg-brand-700 transition-colors"
                >
                  <span>View Guidelines</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                </a>
              </div>
            </div>

            <p className="text-xs text-slate-600 mt-3 leading-relaxed">{scheme.description}</p>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-400 block font-medium">Subsidy Assistance</span>
                <span className="font-bold text-brand-700 text-sm">{scheme.subsidyRate}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-400 block font-medium">Max Project Cap</span>
                <span className="font-bold text-slate-900 text-sm">{scheme.maxProjectCost}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-400 block font-medium">Compliance Readiness</span>
                <span className="font-bold text-emerald-600 text-sm flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  {scheme.status}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

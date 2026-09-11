import React from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { FileSpreadsheet, Download, FileText, CheckCircle2 } from "lucide-react";

export default function ReportsPage() {
  const reports = [
    {
      title: "ThinkForge Comprehensive Project Dossier (PMEGP Compliant)",
      date: "Generated Today • 10 Sep 2026",
      pages: "18 Pages (PDF)",
      type: "Bank-Ready DPR",
      evidence: "VERIFIED" as const,
    },
    {
      title: "Wardha Agro-Processing Feasibility & Sensitivity Analysis",
      date: "08 Sep 2026",
      pages: "12 Pages (PDF)",
      type: "Market Study",
      evidence: "DERIVED" as const,
    },
    {
      title: "Partner Capacity Due-Diligence & Synergy Matrix",
      date: "05 Sep 2026",
      pages: "6 Pages (PDF)",
      type: "Partner Dossier",
      evidence: "VERIFIED" as const,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <FileSpreadsheet className="w-4 h-4 text-brand-600" />
            <span>EXECUTIVE REPORTS & DPRS</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Bankable Project Reports</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Exportable Dossiers</h1>
          <p className="text-sm text-slate-600">
            Download standard bank-ready Detailed Project Reports (DPR), subsidy annexures, and capability scorecards.
          </p>
        </div>

        <button className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all">
          <Download className="w-4 h-4 text-emerald-200" />
          Generate New Bank Dossier
        </button>
      </div>

      <div className="space-y-3">
        {reports.map((report) => (
          <div
            key={report.title}
            className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card hover:border-brand-500 transition-all flex items-center justify-between gap-4"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-brand-50 border border-brand-200/60 flex items-center justify-center text-brand-700 shrink-0">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold text-slate-500">{report.type}</span>
                  <EvidenceBadge type={report.evidence} />
                </div>
                <h3 className="font-bold text-base text-slate-900">{report.title}</h3>
                <p className="text-xs text-slate-500 mt-0.5">{report.date} • {report.pages}</p>
              </div>
            </div>

            <button className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-slate-900 text-white hover:bg-brand-700 transition-colors shrink-0">
              <Download className="w-3.5 h-3.5" />
              <span>Download PDF</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

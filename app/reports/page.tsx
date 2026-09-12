"use client";

import React, { useState } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { FileSpreadsheet, Download, FileText, CheckCircle2, Loader2 } from "lucide-react";

export default function ReportsPage() {
  const [downloading, setDownloading] = useState<string | null>(null);

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

  const parseCurrency = (str: string) => {
    if (!str) return 0;
    return parseInt(str.replace(/[^0-9]/g, "")) || 0;
  };

  const handleDownload = async (title: string) => {
    setDownloading(title);
    
    try {
      // 1. Get Profile
      const storedProfile = localStorage.getItem("thinkforge_profile");
      const name = localStorage.getItem("thinkforge_name") || "Rural Entrepreneur";
      const rawProfile = storedProfile ? JSON.parse(storedProfile) : {};
      
      const profilePayload = {
        user_id: "demo_user",
        name: name,
        available_capital: parseCurrency(rawProfile.ownEquity || "150000"),
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

      // 2. Fetch Opportunities
      const oppsRes = await fetch("http://localhost:8000/api/intelligence/opportunity/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profilePayload)
      });
      const opps = oppsRes.ok ? await oppsRes.json() : [];

      // 3. Fetch Partners
      const partnersRes = await fetch("http://localhost:8000/api/intelligence/partner/recommendations?max_radius_km=50", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profilePayload)
      });
      const partners = partnersRes.ok ? await partnersRes.json() : [];

      // 4. Fetch Finance Simulation
      const financePayload = {
        project_cost: 480000,
        own_contribution: profilePayload.available_capital,
        interest_rate: 8.5,
        tenure_months: 60,
        operating_assumptions: {
          monthly_revenue: 85000,
          monthly_fixed_costs: 20000,
          monthly_variable_costs: 30000
        }
      };
      const financeRes = await fetch("http://localhost:8000/finance/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(financePayload)
      });
      const finance = financeRes.ok ? await financeRes.json() : null;

      // 5. Build Report Content
      let content = `========================================================\n`;
      content += `    THINKFORGE DETAILED PROJECT DOSSIER (DPR)\n`;
      content += `========================================================\n\n`;
      content += `Title: ${title}\n`;
      content += `Generated on: ${new Date().toLocaleString()}\n`;
      content += `Generated for: ${name}\n`;
      content += `Location: ${profilePayload.location.district}, ${profilePayload.location.state}\n\n`;

      content += `--- 1. ENTREPRENEUR PROFILE ---\n`;
      content += `- Declared Equity: ₹${profilePayload.available_capital.toLocaleString()}\n`;
      content += `- Primary Skills: ${profilePayload.skills.join(", ")}\n`;
      content += `- Infrastructure: ${profilePayload.resources.join(", ")}\n\n`;

      content += `--- 2. FEASIBILITY & RECOMMENDED OPPORTUNITIES ---\n`;
      if (opps.length > 0) {
        opps.forEach((o: any, idx: number) => {
          content += `${idx + 1}. ${o.business_name || o.title} (Fit: ${Math.round(o.overall_fit_score)}%)\n`;
          content += `   Sector: ${o.sector}\n`;
          content += `   Required Capital: ₹${(o.capital_required_rec || o.capitalNeeded || 0).toLocaleString()}\n`;
          content += `   Estimated Payback: ${o.estimated_break_even_months || o.payback} Months\n\n`;
        });
      } else {
        content += `No matching opportunities found based on current profile constraints.\n\n`;
      }

      if (finance) {
        content += `--- 3. FINANCIAL STRUCTURING & AMORTIZATION ---\n`;
        content += `- Project Cost: ₹4,80,000\n`;
        content += `- Entrepreneur Contribution: ₹${profilePayload.available_capital.toLocaleString()}\n`;
        content += `- Required Loan (After Subsidy): ₹${Math.round(finance.required_loan).toLocaleString()}\n`;
        content += `- Estimated Bank EMI (8.5% for 5Yrs): ₹${Math.round(finance.emi).toLocaleString()} / month\n`;
        content += `- Projected Monthly Net Surplus: ₹${Math.round(finance.monthly_profit).toLocaleString()} / month\n\n`;
      }

      content += `--- 4. PARTNER ECOSYSTEM & SYNERGIES ---\n`;
      if (partners.length > 0) {
        partners.forEach((p: any, idx: number) => {
          content += `${idx + 1}. ${p.display_title || p.name} (Synergy: ${Math.round(p.synergy_score)}%)\n`;
          content += `   Location: ${p.approximate_area}\n`;
          content += `   Strengths: ${p.key_strengths?.join(", ")}\n`;
          content += `   Value Add: ${p.why_matched?.[0] || "Complementary resources"}\n\n`;
        });
      } else {
        content += `No complementary partners found within a 50km radius.\n\n`;
      }

      content += `========================================================\n`;
      content += `CONFIDENTIAL & AUTO-GENERATED BY THINKFORGE ENGINE\n`;
      content += `========================================================\n`;

      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement("a");
      a.href = url;
      a.download = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.txt`;
      document.body.appendChild(a);
      a.click();
      
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

    } catch (e) {
      console.error("Failed to generate report", e);
    } finally {
      setDownloading(null);
    }
  };

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

        <button 
          onClick={() => handleDownload("ThinkForge_New_Dossier")}
          disabled={downloading !== null}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all disabled:opacity-50"
        >
          {downloading === "ThinkForge_New_Dossier" ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4 text-emerald-200" />}
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

            <button 
              onClick={() => handleDownload(report.title)}
              disabled={downloading === report.title}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-slate-900 text-white hover:bg-brand-700 transition-colors shrink-0 disabled:opacity-70"
            >
              {downloading === report.title ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Download className="w-3.5 h-3.5" />}
              <span>{downloading === report.title ? "Generating..." : "Download"}</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

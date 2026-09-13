"use client";

import React, { useState, useEffect } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { WalletCards, TrendingUp, DollarSign, Calculator, AlertCircle, Loader2 } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

const EmiCalculator = () => {
  const { t } = useLanguage();
  const [principal, setPrincipal] = useState(300000);
  const [rate, setRate] = useState(8.5);
  const [tenureYears, setTenureYears] = useState(5);

  const r = rate / 12 / 100;
  const n = tenureYears * 12;
  const emi = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) || 0;
  const totalAmount = emi * n;
  const totalInterest = totalAmount - principal;

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card h-full">
      <h3 className="font-bold text-base text-slate-900 mb-4 flex items-center gap-2">
        <Calculator className="w-5 h-5 text-brand-600" />
        {t("fin_emi_calc")}
      </h3>
      <div className="space-y-4">
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">{t("fin_loan_amt")} (₹ {principal.toLocaleString()})</label>
          <input type="range" min="10000" max="2000000" step="10000" value={principal} onChange={e => setPrincipal(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">{t("fin_interest_rate")} ({rate}%)</label>
          <input type="range" min="5" max="20" step="0.5" value={rate} onChange={e => setRate(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-600 block mb-1">{t("fin_tenure")} ({tenureYears} {t("fin_years")})</label>
          <input type="range" min="1" max="15" step="1" value={tenureYears} onChange={e => setTenureYears(Number(e.target.value))} className="w-full accent-brand-600" />
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-100">
          <div>
            <p className="text-[11px] text-slate-500 font-medium">{t("fin_monthly_emi")}</p>
            <p className="text-lg font-bold text-emerald-700">₹{Math.round(emi).toLocaleString()}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-500 font-medium">{t("fin_total_interest")}</p>
            <p className="text-lg font-bold text-slate-900">₹{Math.round(totalInterest).toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function FinancePage() {
  const { t } = useLanguage();
  const [profile, setProfile] = useState<any>(null);
  const [simulation, setSimulation] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  const [catalog, setCatalog] = useState<any[]>([]);
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);

  const parseCurrency = (str: string) => {
    if (!str) return 0;
    return parseInt(str.replace(/[^0-9]/g, "")) || 0;
  };

  const runSimulationForBiz = async (bizId: string, currentCatalog: any[], currentProfile: any) => {
    setLoading(true);
    try {
      let projectCost = 480000;
      let monthlyRev = 85000;
      let opCost = 50000;
      let bizName = "Standard Model";

      const biz = currentCatalog.find((b: any) => b.id === bizId);
      if (biz) {
        projectCost = biz.requirements.recommended_capital;
        monthlyRev = biz.requirements.estimated_monthly_revenue;
        opCost = biz.requirements.estimated_monthly_operating_cost;
        bizName = biz.name;
      }

      const ownEquity = parseCurrency(currentProfile?.ownEquity || "150000");
      
      const payload = {
        project_cost: projectCost,
        own_contribution: ownEquity,
        interest_rate: 8.5,
        tenure_months: 60,
        operating_assumptions: {
          monthly_revenue: monthlyRev,
          monthly_fixed_costs: Math.round(opCost * 0.4),
          monthly_variable_costs: Math.round(opCost * 0.6)
        }
      };

      const res = await fetch("http://localhost:8000/finance/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const simData = await res.json();
        setSimulation({ ...simData, _bizName: bizName, _projectCost: projectCost, _monthlyRev: monthlyRev, _opCost: opCost });
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
    const initData = async () => {
      setLoading(true);
      const stored = localStorage.getItem("thinkforge_profile");
      let rawProfile: any = {};
      let currentProfile = null;
      if (stored) {
        rawProfile = JSON.parse(stored);
        currentProfile = rawProfile;
        setProfile(currentProfile);
      }
      
      const backendProfile = {
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

      try {
        const [catRes, oppRes] = await Promise.all([
          fetch("http://localhost:8000/api/intelligence/opportunity/catalog"),
          fetch("http://localhost:8000/api/intelligence/opportunity/recommendations", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(backendProfile)
          })
        ]);

        let catData: any[] = [];
        if (catRes.ok) catData = await catRes.json();
        setCatalog(catData);

        let oppData: any[] = [];
        if (oppRes.ok) oppData = await oppRes.json();
        
        // Take all recommended for tabs
        const topOpps = oppData;
        setOpportunities(topOpps);

        let defaultBizId = topOpps.length > 0 ? topOpps[0].business_id : null;
        if (typeof window !== 'undefined') {
          const searchParams = new URLSearchParams(window.location.search);
          const bizId = searchParams.get('business_id');
          if (bizId) {
             defaultBizId = bizId;
             // Ensure it's in the tabs if possible, otherwise it will just simulate
             if (!topOpps.find(o => o.business_id === bizId) && catData.find(c => c.id === bizId)) {
                const b = catData.find(c => c.id === bizId);
                setOpportunities([{ business_id: b.id, business_name: b.name }, ...topOpps]);
             }
          }
        }
        
        if (defaultBizId) {
           setActiveTabId(defaultBizId);
           await runSimulationForBiz(defaultBizId, catData, currentProfile);
        } else {
           setLoading(false);
        }

      } catch (e) {
        console.error(e);
        setLoading(false);
      }
    };
    initData();
  }, []);

  const handleTabClick = (bizId: string) => {
    setActiveTabId(bizId);
    runSimulationForBiz(bizId, catalog, profile);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <WalletCards className="w-4 h-4 text-brand-600" />
            <span>{t("fin_structuring")}</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">{t("fin_capex_sim")}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">{t("fin_architecture")}</h1>
          <p className="text-sm text-slate-600">
            {t("fin_arch_desc")}
          </p>
        </div>

        <button 
          onClick={() => activeTabId && runSimulationForBiz(activeTabId, catalog, profile)}
          disabled={loading}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all disabled:opacity-70"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Calculator className="w-4 h-4 text-emerald-200" />}
          {t("fin_refresh_sim")}
        </button>
      </div>

      {/* Tabs */}
      {opportunities.length > 0 && (
        <div className="flex overflow-x-auto hide-scrollbar gap-2 pb-1 border-b border-slate-200">
          {opportunities.map((opp) => (
            <button
              key={opp.business_id}
              onClick={() => handleTabClick(opp.business_id)}
              className={`whitespace-nowrap px-4 py-2.5 rounded-t-xl text-sm font-semibold transition-all border-b-2 ${
                activeTabId === opp.business_id 
                  ? "bg-brand-50 text-brand-700 border-brand-600" 
                  : "text-slate-500 border-transparent hover:text-slate-800 hover:bg-slate-50"
              }`}
            >
              {opp.business_name || opp.title}
            </button>
          ))}
        </div>
      )}

      {loading && !simulation ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500 mb-4" />
          <p>{t("fin_running_sim")}</p>
        </div>
      ) : simulation ? (
        <div className="space-y-6 animate-in fade-in duration-300">
          {/* Financial Snapshot KPI Tiles */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">{t("fin_proj_cost")}</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">₹{simulation._projectCost?.toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-emerald-700 font-semibold truncate max-w-[120px]">{t(simulation._bizName || "fin_standard_model")}</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">{t("fin_own_equity")}</span>
              <p className="text-2xl font-bold text-brand-700 mt-1">₹{parseCurrency(profile?.ownEquity || "150000").toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-slate-600 font-semibold">{t("fin_user_declared")}</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">{t("fin_req_loan")}</span>
              <p className="text-2xl font-bold text-emerald-600 mt-1">₹{Math.round(simulation.required_loan).toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-emerald-700 font-semibold">{t("fin_after_subsidy")}</span>
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-card">
              <span className="text-xs font-medium text-slate-500">{t("fin_est_emi")}</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">₹{Math.round(simulation.emi).toLocaleString()}</p>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-slate-600 font-semibold">{t("fin_at_85_5yr")}</span>
                <EvidenceBadge type="DERIVED" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
            {/* Pro-forma Cash Flow Table */}
            <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-card h-full">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-slate-900">{t("fin_proj_cash_flow")}</h3>
                <span className="text-xs text-slate-500">{t("fin_assumes_75")}</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                      <th className="pb-3">{t("fin_metric")}</th>
                      <th className="pb-3 text-right">{t("fin_monthly_avg")}</th>
                      <th className="pb-3 text-right">{t("fin_yr1_total")}</th>
                      <th className="pb-3 text-right">{t("fin_evidence_level")}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-slate-700 font-medium">
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">{t("fin_gross_sales")}</td>
                      <td className="py-3 text-right">₹{simulation._monthlyRev?.toLocaleString()}</td>
                      <td className="py-3 text-right">₹{(simulation._monthlyRev * 12)?.toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
                    </tr>
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">{t("fin_total_op_costs")}</td>
                      <td className="py-3 text-right">₹{simulation._opCost?.toLocaleString()}</td>
                      <td className="py-3 text-right">₹{(simulation._opCost * 12)?.toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="ESTIMATED" /></td>
                    </tr>
                    <tr>
                      <td className="py-3 font-semibold text-slate-900">{t("fin_loan_repayment")}</td>
                      <td className="py-3 text-right">₹{Math.round(simulation.emi).toLocaleString()}</td>
                      <td className="py-3 text-right">₹{Math.round(simulation.emi * 12).toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="VERIFIED" /></td>
                    </tr>
                    <tr className="bg-emerald-50/50">
                      <td className="py-3 font-bold text-emerald-900">{t("fin_net_surplus")}</td>
                      <td className="py-3 text-right font-bold text-emerald-800">₹{Math.round(simulation.monthly_profit).toLocaleString()}</td>
                      <td className="py-3 text-right font-bold text-emerald-800">₹{Math.round(simulation.monthly_profit * 12).toLocaleString()}</td>
                      <td className="py-3 text-right"><EvidenceBadge type="DERIVED" /></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Quick EMI Calculator */}
            <div className="lg:col-span-1 h-full">
              <EmiCalculator />
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

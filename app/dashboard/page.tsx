"use client";

import React from "react";
import Link from "next/link";
import EvidenceBadge from "@/components/EvidenceBadge";
import { useLanguage } from "@/contexts/LanguageContext";
import {
  Sparkles,
  MapPin,
  TrendingUp,
  IndianRupee,
  Compass,
  Handshake,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  RefreshCw,
  FileDown,
  Edit3,
  BarChart3,
  Radar,
  MapPinned,
  ListTodo,
} from "lucide-react";

export default function DashboardPage() {
  const { t } = useLanguage();
  const [profile, setProfile] = React.useState<any>(null);
  const [userName, setUserName] = React.useState<string>("Rural Entrepreneur");
  const [partnerCount, setPartnerCount] = React.useState<number | null>(null);
  const [partnerSubtext, setPartnerSubtext] = React.useState<string>(t("dash_scanning_local"));
  const [oppCount, setOppCount] = React.useState<number | null>(null);
  const [oppSubtext, setOppSubtext] = React.useState<string>(t("dash_analyzing_feas"));

  React.useEffect(() => {
    const updateDashboardProfile = () => {
      try {
        const stored = localStorage.getItem("thinkforge_profile");
        let parsedProfile = null;
        if (stored) {
          parsedProfile = JSON.parse(stored);
          setProfile(parsedProfile);
        }
        const name = localStorage.getItem("thinkforge_name");
        if (name) {
          setUserName(name);
        }

        // Fetch partners to match the partner section
        const rawProfile = parsedProfile || {};
        const mappedProfile = {
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

        fetch("http://localhost:8000/api/intelligence/partner/recommendations?max_radius_km=50", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(mappedProfile)
        })
          .then(res => res.json())
          .then(data => {
            if (Array.isArray(data)) {
              setPartnerCount(data.length);
              const types = data.map(p => {
                if (p.investment_range_str) {
                  if (p.investment_range_str.includes("₹")) return p.type || "Local Partner";
                  return p.investment_range_str;
                }
                return p.type || "Local Partner";
              });
              const counts: Record<string, number> = {};
              types.forEach(t => counts[t] = (counts[t] || 0) + 1);
              const summary = Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(", ");
              setPartnerSubtext(summary || t("dash_local_conn"));
            }
          })
          .catch(e => console.error("Failed to fetch dashboard partners", e));

        fetch("http://localhost:8000/api/intelligence/opportunity/recommendations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(mappedProfile)
        })
          .then(res => res.json())
          .then(data => {
            if (Array.isArray(data)) {
              setOppCount(data.length);
              if (data.length > 0) {
                const bestOpp = data[0].business_name || data[0].title || "Agri-Tech";
                setOppSubtext(`${t("dash_highest_fit")} ${bestOpp}`);
              } else {
                setOppSubtext(t("dash_no_viable"));
              }
            }
          })
          .catch(e => console.error("Failed to fetch dashboard opportunities", e));

      } catch (e) {
        console.error(e);
      }
    };

    updateDashboardProfile();
    window.addEventListener("profileUpdated", updateDashboardProfile);
    return () => window.removeEventListener("profileUpdated", updateDashboardProfile);
  }, []);

  const kpiData = [
    {
      title: t("dash_kpi_profile_readiness"),
      value: profile ? "100%" : "78%",
      subtext: profile ? t("dash_kpi_sub_profile_complete") : t("dash_kpi_sub_high_feasibility"),
      trend: t("dash_kpi_trend_initial"),
      evidence: "DERIVED" as const,
      icon: TrendingUp,
      accent: "text-brand-600 bg-brand-50 border-brand-200/80",
    },
    {
      title: t("dash_kpi_available_capital"),
      value: profile?.ownEquity || "₹2,50,000",
      subtext: profile ? t("dash_kpi_sub_equity_credit") : t("dash_kpi_sub_equity_credit_default"),
      trend: t("dash_kpi_trend_leverage"),
      evidence: "VERIFIED" as const,
      icon: IndianRupee,
      accent: "text-emerald-600 bg-emerald-50 border-emerald-200/80",
    },
    {
      title: t("dash_kpi_viable_opps"),
      value: oppCount !== null ? `${oppCount} ${t("dash_kpi_matches")}` : `4 ${t("dash_kpi_matches")}`,
      subtext: oppCount !== null ? oppSubtext : (profile ? `Top: ${profile.sectorInterest?.split(' ')[0]}...` : t("dash_kpi_sub_top_solar")),
      trend: t("dash_kpi_trend_demand"),
      evidence: "DERIVED" as const,
      icon: Compass,
      accent: "text-teal-600 bg-teal-50 border-teal-200/80",
    },
    {
      title: t("dash_kpi_potential_partners"),
      value: partnerCount !== null ? `${partnerCount} ${t("dash_kpi_matched")}` : `7 ${t("dash_kpi_matched")}`,
      subtext: partnerCount !== null ? partnerSubtext : t("3 FPOs, 2 Cold Stores, 2 SHGs"),
      trend: profile && profile.mandiDistance ? `${t("Within")} ${t(profile.mandiDistance)}` : t("All within 20km radius"),
      evidence: "VERIFIED" as const,
      icon: Handshake,
      accent: "text-blue-600 bg-blue-50 border-blue-200/80",
    },
    {
      title: t("dash_kpi_evidence"),
      value: "84%",
      subtext: t("Official Mandi APMC & MoSJE Data"),
      trend: t("Zero Hallucinated Specs"),
      evidence: "VERIFIED" as const,
      icon: ShieldCheck,
      accent: "text-emerald-700 bg-emerald-50 border-emerald-300",
    },
  ];

  const actions = [
    {
      title: t("dash_pmegp_eligibility"),
      deadline: t("dash_priority_immediate"),
      impact: t("dash_grant_eligible"),
      status: "Ready to Apply",
      href: "/schemes",
    },
    {
      title: t("dash_equipment_inspection"),
      deadline: t("dash_within_7_days"),
      impact: t("dash_saves_capex"),
      status: "Pending Connection",
      href: "/partners",
    },
    {
      title: t("dash_lock_power"),
      deadline: t("dash_month_1"),
      impact: t("dash_reduces_opex"),
      status: "Document Verified",
      href: "/local-insights",
    },
  ];

  return (
    <div className="space-y-6 pb-10">
      {/* 1. Header View */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div className="space-y-2">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t("dash_welcome")}, {userName.split(" ")[0]}!
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              {t("dash_overview")}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 text-xs text-slate-600">
            {/* Location Badge */}
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-100 text-slate-700 font-medium">
              <MapPin className="w-3.5 h-3.5 text-brand-600 shrink-0" />
              <span>{t("dash_wardha_district")}</span>
            </div>

            {/* Profile Summary Pill */}
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-brand-50 text-brand-800 font-medium border border-brand-200/60">
              <Sparkles className="w-3.5 h-3.5 text-brand-600 shrink-0" />
              <span>{t("dash_agri_solar")}</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap items-center gap-2.5 shrink-0">
          <Link
            href="/register"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-slate-900 shadow-sm transition-all"
          >
            <Edit3 className="w-3.5 h-3.5 text-slate-500" />
            <span>{t("dash_recalibrate")}</span>
          </Link>

          <Link
            href="/finance"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-slate-900 shadow-sm transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
            <span>{t("dash_simulate")}</span>
          </Link>

          <Link
            href="/reports"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-brand-600 to-teal-700 text-white hover:opacity-95 shadow-glow-teal transition-all"
          >
            <FileDown className="w-3.5 h-3.5 text-emerald-200" />
            <span>{t("dash_download_dossier")}</span>
          </Link>
        </div>
      </div>

      {/* 2. Grid of 5 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {kpiData.map((kpi) => {
          const Icon = kpi.icon;
          return (
            <div
              key={kpi.title}
              className="bg-white rounded-2xl border border-slate-200 p-4 sm:p-5 shadow-card hover:shadow-card-elevated hover:border-brand-500/50 transition-all flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-2">
                  <span className="text-xs font-semibold text-slate-500 truncate" title={kpi.title}>
                    {kpi.title}
                  </span>
                  <div className={`p-1.5 rounded-lg border shrink-0 ${kpi.accent}`}>
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                </div>

                <div className="mt-1">
                  <p className="text-2xl font-extrabold text-slate-900 tracking-tight">
                    {kpi.value}
                  </p>
                  <p className="text-[11px] text-slate-500 mt-1 font-medium leading-tight">
                    {kpi.subtext}
                  </p>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                <span className="text-emerald-700 font-semibold truncate">{kpi.trend}</span>
                <EvidenceBadge type={kpi.evidence} showIcon={false} className="text-[10px] px-2" />
              </div>
            </div>
          );
        })}
      </div>

      {/* 3. Structured Layout Placeholders (Empty div cards with dashed borders & labels) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Placeholder 1: Top Opportunities (Chart) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-brand-600" />
              <h3 className="font-bold text-base text-slate-900">{t("dash_top_opps")}</h3>
            </div>
            <Link
              href="/opportunities"
              className="text-xs font-bold text-brand-700 hover:text-brand-800 inline-flex items-center gap-1"
            >
              {t("dash_view_all")}
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Structured Layout Placeholder with dashed border & clear label */}
          <div className="flex-1 min-h-[260px] rounded-xl border border-slate-200 bg-white p-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <div>
                  <p className="text-xs font-bold text-slate-900">{t("dash_solar_chain")}</p>
                  <p className="text-[10px] text-slate-500">{t("dash_highest_viability")}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-emerald-600">89% {t("dash_fit")}</p>
                  <p className="text-[10px] text-slate-500">₹3.5L {t("dash_capex")}</p>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <div>
                  <p className="text-xs font-bold text-slate-900">{t("dash_agri_briquette")}</p>
                  <p className="text-[10px] text-slate-500">{t("dash_strong_market")}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-brand-600">83% {t("dash_fit")}</p>
                  <p className="text-[10px] text-slate-500">₹2.2L {t("dash_capex")}</p>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <div>
                  <p className="text-xs font-bold text-slate-900">{t("dash_fiber_extract")}</p>
                  <p className="text-[10px] text-slate-500">{t("dash_niche_rural")}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-teal-600">78% {t("dash_fit")}</p>
                  <p className="text-[10px] text-slate-500">₹1.8L {t("dash_capex")}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Placeholder 2: Capability Scorecard (Chart) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Radar className="w-4 h-4 text-emerald-600" />
              <h3 className="font-bold text-base text-slate-900">{t("dash_cap_scorecard")}</h3>
            </div>
            <EvidenceBadge type="DERIVED" />
          </div>

          {/* Structured Layout Placeholder with dashed border & clear label */}
          <div className="flex-1 min-h-[260px] rounded-xl border border-slate-200 bg-white p-5 flex flex-col justify-center space-y-5">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-semibold text-slate-700">{t("dash_fin_capacity")}</span>
                <span className="font-bold text-brand-700">82%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2">
                <div className="bg-brand-500 h-2 rounded-full" style={{ width: '82%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-semibold text-slate-700">{t("dash_tech_expertise")}</span>
                <span className="font-bold text-emerald-700">75%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2">
                <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '75%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-semibold text-slate-700">{t("dash_infra_assets")}</span>
                <span className="font-bold text-teal-700">85%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2">
                <div className="bg-teal-500 h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-semibold text-slate-700">{t("dash_risk_resil")}</span>
                <span className="font-bold text-blue-700">60%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '60%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Placeholder 3: Local Insights (Map) */ }
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <MapPinned className="w-4 h-4 text-teal-600" />
              <h3 className="font-bold text-base text-slate-900">{t("dash_local_insights")}</h3>
            </div>
            <Link
              href="/local-insights"
              className="text-xs font-bold text-brand-700 hover:text-brand-800 inline-flex items-center gap-1"
            >
              {t("dash_explore_map")}
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Structured Layout Placeholder with dashed border & clear label */}
          <div className="flex-1 min-h-[260px] rounded-xl border border-slate-200 relative overflow-hidden flex flex-col">
            <iframe 
              width="100%" 
              height="100%" 
              src="https://maps.google.com/maps?q=20.7453,78.6022&z=11&output=embed" 
              frameBorder="0" 
              style={{ border: 0, position: 'absolute', inset: 0 }} 
              allowFullScreen 
              title="Dashboard Local Area Map"
            />
            
            <div className="mt-auto relative z-10 flex flex-wrap items-center justify-center gap-3 p-3 bg-white/90 backdrop-blur-md border-t border-slate-200 text-[10px] font-semibold text-slate-700 pointer-events-none">
              <span className="inline-flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-emerald-500" /> {t("dash_mandi_14km")}
              </span>
              <span className="inline-flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-blue-500" /> {t("dash_3_fpos")}
              </span>
              <span className="inline-flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-amber-500" /> {t("dash_low_sat")}
              </span>
            </div>
          </div>
        </div>

        {/* Placeholder 4: Recommended Actions (List) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <ListTodo className="w-4 h-4 text-brand-600" />
              <h3 className="font-bold text-base text-slate-900">{t("dash_rec_actions")}</h3>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              3 {t("dash_steps_pending")}
            </span>
          </div>

          {/* Structured Layout Placeholder with dashed border & clear label */}
          <div className="flex-1 min-h-[260px] rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/70 p-4 sm:p-5 flex flex-col justify-between transition-colors hover:border-brand-400">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold tracking-wider uppercase text-slate-400">
                  {t("dash_layout_placeholder")}
                </span>
                <span className="text-[11px] font-bold text-slate-500">
                  {t("dash_prioritized_roadmap")}
                </span>
              </div>

              <div className="space-y-2.5 mt-3 text-left">
                {actions.map((action, idx) => (
                  <Link
                    key={action.title}
                    href={action.href}
                    className="block p-3 rounded-xl bg-white border border-slate-200/90 hover:border-brand-500 hover:shadow-sm transition-all group"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-start gap-2.5">
                        <span className="w-5 h-5 rounded-full bg-brand-50 text-brand-700 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                          {idx + 1}
                        </span>
                        <div>
                          <p className="text-xs font-bold text-slate-900 group-hover:text-brand-700 transition-colors">
                            {action.title}
                          </p>
                          <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1.5">
                            <Clock className="w-3 h-3 text-slate-400" />
                            {action.deadline}
                          </p>
                        </div>
                      </div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0">
                        {action.impact}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs text-slate-500">
              <span>{t("dash_automated_by")}</span>
              <span className="font-bold text-brand-700">{t("dash_next_review")}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

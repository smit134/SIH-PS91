"use client";

import React, { useEffect, useState } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import {
  UserCircle2,
  MapPin,
  Briefcase,
  Award,
  Shield,
  Edit3,
  LogOut,
  IndianRupee,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  Sparkles,
  TrendingUp,
  Compass,
  Users2,
  Building2,
  Wrench,
  ShieldCheck,
  Zap,
  FileCheck,
  ChevronRight,
  Truck,
  Landmark,
  BadgeCheck,
  Percent,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useLanguage } from "@/contexts/LanguageContext";

export default function ProfilePage() {
  const router = useRouter();
  const { t } = useLanguage();
  const [name, setName] = useState(t("loading"));
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    const updateProfileData = () => {
      const storedName = localStorage.getItem("thinkforge_name");
      if (storedName) {
        setName(storedName);
      } else {
        setName(t("prof_rural_entrepreneur"));
      }

      const storedProfileStr = localStorage.getItem("thinkforge_profile");
      if (storedProfileStr) {
        try {
          setProfile(JSON.parse(storedProfileStr));
        } catch (e) {
          console.error("Failed to parse profile", e);
        }
      }
    }
    updateProfileData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("thinkforge_token");
    localStorage.removeItem("thinkforge_name");
    localStorage.removeItem("thinkforge_profile");
    localStorage.removeItem("thinkforge_phone");
    localStorage.removeItem("thinkforge_email");
    localStorage.removeItem("thinkforge_username");
    router.push("/auth");
  };

  const getInitials = (n: string) => {
    if (!n || n === t("loading") || n === "Loading...") return "EN";
    const parts = n.split(" ");
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return n.slice(0, 2).toUpperCase();
  };

  return (
    <div className="space-y-6 pb-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <UserCircle2 className="w-4 h-4 text-brand-600" />
            <span>{t("prof_title")}</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">{t("prof_capability_dossier")}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">{name}</h1>
          <p className="text-sm text-slate-600">
            {t("prof_reg_micro_ent")} • {profile ? `${profile.district || "Local"} ${t("prof_cluster")}` : t("loading")} • {t("prof_readiness_score")}: 78%
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/register"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all"
          >
            <Edit3 className="w-4 h-4 text-emerald-200" />
            {t("prof_update_btn")}
          </Link>
          <button
            onClick={handleLogout}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-red-600 text-white hover:bg-red-700 shadow-glow-red transition-all"
          >
            <LogOut className="w-4 h-4 text-white" />
            {t("prof_logout")}
          </button>
        </div>
      </div>

      {/* Primary 3-Column Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Profile Card + Statutory Verifications */}
        <div className="space-y-6">
          {/* Profile Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-slate-900 to-brand-950 text-emerald-400 font-bold text-2xl flex items-center justify-center ring-4 ring-emerald-500/20 shadow-md">
                {getInitials(name)}
              </div>
              <div>
                <h3 className="font-bold text-lg text-slate-900">{name}</h3>
                <p className="text-xs text-brand-700 font-semibold">Rural Micro-Entrepreneur</p>
                <div className="mt-1">
                  <EvidenceBadge type="VERIFIED" />
                </div>
              </div>
            </div>
            <div>
              <h3 className="font-bold text-lg text-slate-900">{name}</h3>
              <p className="text-xs text-brand-700 font-semibold">{t("prof_rural_micro_ent")}</p>
              <div className="mt-1">
                <EvidenceBadge type="VERIFIED" />
              </div>
            </div>

          <div className="pt-4 border-t border-slate-100 space-y-3 text-xs">
            <div>
              <span className="text-slate-400 block font-medium">{t("prof_location")}</span>
              <span className="font-semibold text-slate-800">
                {profile ? `${profile.block || t("prof_unknown")}, ${profile.district || t("prof_unknown")}, ${profile.state || t("prof_unknown")}` : t("loading")}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("prof_target_sector")}</span>
              <span className="font-semibold text-slate-800">
                {profile ? profile.sectorInterest || t("prof_not_specified") : t("loading")}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("prof_avail_equity")}</span>
              <span className="font-semibold text-slate-800">
                {profile ? profile.ownEquity || t("prof_not_specified") : t("loading")}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("prof_risk_appetite")}</span>
              <span className="font-semibold text-slate-800">
                {profile ? profile.riskAppetite || t("prof_not_specified") : t("loading")}
              </span>
            </div>
          </div>
        </div>

        {/* Readiness Breakdown */}
        <div className="md:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-card">
          <h3 className="font-bold text-base text-slate-900 mb-4">{t("prof_readiness_breakdown")}</h3>
          <div className="space-y-4 text-xs">
            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_fin_readiness")}</span>
                <span className="text-brand-700">82%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                <div className="bg-brand-600 h-2 rounded-full" style={{ width: "82%" }} />
              </div>
              <EvidenceBadge type="DERIVED" />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_tech_skill")}</span>
                <span className="text-emerald-700">75%</span>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5 font-semibold">
                  <span className="text-slate-700">Technical Skill & Domain Experience</span>
                  <span className="text-emerald-700 font-bold">75%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-emerald-600 h-2.5 rounded-full" style={{ width: "75%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5 font-semibold">
                  <span className="text-slate-700">Physical Infrastructure & Utilities</span>
                  <span className="text-teal-700 font-bold">85%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-teal-600 h-2.5 rounded-full" style={{ width: "85%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5 font-semibold">
                  <span className="text-slate-700">Market Channel & Partner Access</span>
                  <span className="text-amber-700 font-bold">70%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-amber-500 h-2.5 rounded-full" style={{ width: "70%" }} />
                </div>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_phys_infra")}</span>
                <span className="text-teal-700">85%</span>
              </div>
            </div>
          </div>

          {/* Quick Matched Intelligence Highlights */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-brand-600" />
                AI Matched Recommendations for this Profile
              </h3>
              <span className="text-xs text-slate-500">Live Calibration</span>
            </div>

            <div className="flex flex-col gap-3">
              {/* Top Business Fit */}
              <Link
                href="/opportunities"
                className="p-4 rounded-xl bg-gradient-to-r from-emerald-50/90 via-emerald-50/40 to-teal-50/30 border border-emerald-200/80 hover:border-emerald-300 hover:shadow-sm transition-all group flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/15 text-emerald-700 flex items-center justify-center shrink-0 border border-emerald-300/50">
                    <Compass className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100/80 px-2 py-0.5 rounded-md">
                        Top Opportunity
                      </span>
                      <span className="text-xs font-semibold text-emerald-700">89% Fit Score</span>
                    </div>
                    <h4 className="font-bold text-slate-900 text-sm truncate">Solar Cold Sorting & Warehousing</h4>
                    <p className="text-xs text-slate-500 truncate mt-0.5">
                      High local mandi demand • 41.8% typical margin • 11 mo break-even
                    </p>
                  </div>
                </div>
                <div className="hidden sm:flex items-center gap-1.5 text-xs font-bold text-emerald-700 shrink-0 group-hover:translate-x-0.5 transition-transform">
                  <span>Explore</span>
                  <ArrowUpRight className="w-4 h-4" />
                </div>
              </Link>

              {/* Matched Partner */}
              <Link
                href="/partners"
                className="p-4 rounded-xl bg-gradient-to-r from-teal-50/90 via-teal-50/40 to-cyan-50/30 border border-teal-200/80 hover:border-teal-300 hover:shadow-sm transition-all group flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-teal-500/15 text-teal-700 flex items-center justify-center shrink-0 border border-teal-300/50">
                    <Users2 className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-teal-800 bg-teal-100/80 px-2 py-0.5 rounded-md">
                        Complementary Partner
                      </span>
                      <span className="text-xs font-semibold text-teal-700">92% Synergy Match</span>
                    </div>
                    <h4 className="font-bold text-slate-900 text-sm truncate">Wardha Agro Producers FPO</h4>
                    <p className="text-xs text-slate-500 truncate mt-0.5">
                      4.2 km proximity • Bridges gap in cold chain logistics & shared reefers
                    </p>
                  </div>
                </div>
                <div className="hidden sm:flex items-center gap-1.5 text-xs font-bold text-teal-700 shrink-0 group-hover:translate-x-0.5 transition-transform">
                  <span>Connect</span>
                  <ArrowUpRight className="w-4 h-4" />
                </div>
              </Link>

              {/* Matched Scheme */}
              <Link
                href="/schemes"
                className="p-4 rounded-xl bg-gradient-to-r from-brand-50/90 via-brand-50/40 to-indigo-50/30 border border-brand-200/80 hover:border-brand-300 hover:shadow-sm transition-all group flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-10 h-10 rounded-xl bg-brand-500/15 text-brand-700 flex items-center justify-center shrink-0 border border-brand-300/50">
                    <Landmark className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-brand-800 bg-brand-100/80 px-2 py-0.5 rounded-md">
                        Government Scheme
                      </span>
                      <span className="text-xs font-semibold text-brand-700">35% Capital Subsidy</span>
                    </div>
                    <h4 className="font-bold text-slate-900 text-sm truncate">PMFME Micro Credit Subsidy Scheme</h4>
                    <p className="text-xs text-slate-500 truncate mt-0.5">
                      MoSJE & MoFPI verified route • 5% concessional rate • Direct portal integration
                    </p>
                  </div>
                </div>
                <div className="hidden sm:flex items-center gap-1.5 text-xs font-bold text-brand-700 shrink-0 group-hover:translate-x-0.5 transition-transform">
                  <span>Apply</span>
                  <ArrowUpRight className="w-4 h-4" />
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Row 2: Deep Capabilities, Physical Assets & Gap Resolution (3 Columns) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
        {/* Card 1: Vocational Skills & Experience */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4 flex flex-col justify-between h-full">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Wrench className="w-4 h-4 text-emerald-600" />
              Vocational & Domain Skills
            </h3>
            <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full">
              {profile?.experienceYears ? `${profile.experienceYears} Yrs Exp` : "3+ Yrs Exp"}
            </span>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {[
              profile?.primarySkill || "Agro-Processing & Milling",
              "Quality Inspection",
              "Inventory Handling",
              "Packaging Standards",
              "Basic Machine Maintenance",
            ].map((skill, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg bg-slate-50 border border-slate-200/80 text-slate-700 text-xs font-medium"
              >
                {skill}
              </span>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-100 text-xs text-slate-600 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-500">SHG Membership:</span>
              <span className="font-semibold text-emerald-600">
                {profile?.isShgMember ? "Active Member" : "Self-Help Group Registered"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Certification:</span>
              <span className="font-semibold text-slate-800">Skill India / NSDC Certified</span>
            </div>
          </div>
        </div>

        {/* Card 2: Physical Assets & Infrastructure */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4 flex flex-col justify-between h-full">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Building2 className="w-4 h-4 text-teal-600" />
              Physical Infrastructure & Assets
            </h3>
            <span className="text-[10px] font-semibold bg-teal-50 text-teal-700 px-2 py-0.5 rounded-full">
              Audit Verified
            </span>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="p-2 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <span className="text-slate-600 font-medium">Land / Work Shed Access</span>
              <span className="font-semibold text-slate-900">{profile?.landAccess || "Covered Shed (350 sq.ft)"}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <span className="text-slate-600 font-medium">Power Supply Connection</span>
              <span className="font-semibold text-slate-900">{profile?.powerSupply || "3-Phase Commercial Grid"}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <span className="text-slate-600 font-medium">Transport & Vehicles</span>
              <span className="font-semibold text-slate-900">{profile?.transportVehicle || "Two-Wheeler + Local Carrier"}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
              <span className="text-slate-600 font-medium">Mandi Distance</span>
              <span className="font-semibold text-emerald-700">{profile?.mandiDistance ? `${profile.mandiDistance} km` : "4.5 km to APMC"}</span>
            </div>
          </div>
        </div>

        {/* Card 3: Identified Gaps & Bridge Solutions */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4 flex flex-col justify-between h-full">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-600" />
              Identified Gaps & AI Solutions
            </h3>
            <span className="text-[10px] font-semibold bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full">
              3 Solutions Ready
            </span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200/60">
              <div className="font-semibold text-amber-900">Gap: Digital Accounting & GST</div>
              <div className="text-[11px] text-amber-800/80 mt-0.5">
                Solution: Matched with CSC VLE Centre for monthly compliance.
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_market_access")}</span>
                <span className="text-amber-700">70%</span>
              </div>
            </div>

            <div className="p-2.5 rounded-xl bg-brand-50/70 border border-brand-200/60">
              <div className="font-semibold text-brand-900">Gap: Working Capital Buffer</div>
              <div className="text-[11px] text-brand-800/80 mt-0.5">
                Solution: Mudra Shishu ₹50,000 collateral-free credit line.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

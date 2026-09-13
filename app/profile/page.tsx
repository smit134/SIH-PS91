"use client";

import React, { useEffect, useState } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { UserCircle2, MapPin, Briefcase, Award, Shield, Edit3, LogOut } from "lucide-react";
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
    <div className="space-y-6">
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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-card space-y-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-slate-900 to-brand-950 text-emerald-400 font-bold text-2xl flex items-center justify-center ring-4 ring-emerald-500/20">
              {getInitials(name)}
            </div>
            <div>
              <h3 className="font-bold text-lg text-slate-900">{name}</h3>
              <p className="text-xs text-brand-700 font-semibold">{t("prof_rural_micro_ent")}</p>
              <div className="mt-1">
                <EvidenceBadge type="VERIFIED" />
              </div>
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
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_tech_skill")}</span>
                <span className="text-emerald-700">75%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                <div className="bg-emerald-600 h-2 rounded-full" style={{ width: "75%" }} />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_phys_infra")}</span>
                <span className="text-teal-700">85%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                <div className="bg-teal-600 h-2 rounded-full" style={{ width: "85%" }} />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5 font-semibold">
                <span className="text-slate-700">{t("prof_market_access")}</span>
                <span className="text-amber-700">70%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                <div className="bg-amber-500 h-2 rounded-full" style={{ width: "70%" }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

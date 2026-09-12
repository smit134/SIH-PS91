"use client";

import React from "react";
import Link from "next/link";
import {
  Sparkles,
  ShieldCheck,
  MapPin,
  Landmark,
  Compass,
  Users2,
  WalletCards,
  FileSpreadsheet,
  Heart,
  ExternalLink,
} from "lucide-react";

interface FooterProps {
  dark?: boolean;
}

export default function Footer({ dark = false }: FooterProps) {
  const currentYear = new Date().getFullYear();

  if (dark) {
    return (
      <footer className="border-t border-slate-800/80 bg-slate-950 text-slate-400 text-xs py-8 px-6 transition-colors">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-600 to-emerald-600 flex items-center justify-center text-white shadow-glow-teal">
              <Sparkles className="w-4 h-4 text-emerald-200" />
            </div>
            <div>
              <div className="font-bold text-sm text-white flex items-center gap-2">
                Think<span className="text-brand-400">Forge</span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-brand-950 text-brand-400 border border-brand-800/80">
                  SIH26091
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Ministry of Social Justice and Empowerment (MoSJE) • AI Rural Business Advisory
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-6 text-slate-400">
            <Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link>
            <Link href="/opportunities" className="hover:text-white transition-colors">Opportunities</Link>
            <Link href="/partners" className="hover:text-white transition-colors">Partners</Link>
            <Link href="/schemes" className="hover:text-white transition-colors">Government Schemes</Link>
            <Link href="/finance" className="hover:text-white transition-colors">Finance Simulator</Link>
          </div>

          <div className="text-[11px] text-slate-500 text-center md:text-right">
            © {currentYear} ThinkForge. Empowering Rural Micro-Entrepreneurs.
          </div>
        </div>
      </footer>
    );
  }

  return (
    <footer className="border-t border-slate-200/80 bg-white text-slate-600 text-xs mt-auto transition-colors">
      {/* Top Banner with Badges & Trust signals */}
      <div className="border-b border-slate-100 bg-slate-50/50 py-3.5 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-[11px]">
          <div className="flex items-center gap-2 text-slate-700">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="font-semibold text-slate-800">ThinkForge Advisory Engine</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">PostGIS Geospatial Active</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Evidence Classification Engine</span>
          </div>

          <div className="flex items-center gap-4 text-slate-600">
            <span className="flex items-center gap-1 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              Privacy-Masked Contacts
            </span>
            <span className="hidden sm:inline text-slate-300">•</span>
            <span className="hidden sm:flex items-center gap-1 font-medium">
              <Landmark className="w-3.5 h-3.5 text-brand-600" />
              MoSJE Scheme Integrated
            </span>
          </div>
        </div>
      </div>

      {/* Main Footer Links & Info Grid */}
      <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Col 1: About Platform */}
          <div className="space-y-3 md:col-span-1">
            <Link href="/dashboard" className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-600 to-emerald-700 flex items-center justify-center text-white shadow-sm">
                <Sparkles className="w-4 h-4 text-emerald-100" />
              </div>
              <span className="font-bold text-base text-slate-900">
                Think<span className="text-brand-600">Forge</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-brand-50 text-brand-700 border border-brand-200/80 px-1.5 py-0.5 rounded">
                SIH26091
              </span>
            </Link>
            <p className="text-xs text-slate-500 leading-relaxed">
              AI-driven hyper-local rural entrepreneurship decision-support platform. Evaluating localized feasibility, complementary partners, financial structuring, and government scheme routing.
            </p>
            <div className="pt-1 flex items-center gap-2 text-[11px] font-semibold text-slate-700">
              <MapPin className="w-3.5 h-3.5 text-emerald-600" />
              <span>National Rural Clusters Coverage</span>
            </div>
          </div>

          {/* Col 2: Core Platform Modules */}
          <div className="space-y-3">
            <h4 className="font-bold text-slate-900 uppercase text-[11px] tracking-wider">
              Advisory Modules
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/dashboard" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Overview Dashboard</span>
                </Link>
              </li>
              <li>
                <Link href="/opportunities" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>7-Factor Opportunity Fit</span>
                </Link>
              </li>
              <li>
                <Link href="/partners" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Complementary Partner Match</span>
                </Link>
              </li>
              <li>
                <Link href="/finance" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Financial Viability & EMI</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Schemes & Intelligence */}
          <div className="space-y-3">
            <h4 className="font-bold text-slate-900 uppercase text-[11px] tracking-wider">
              Schemes & Analytics
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/schemes" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>PMFME & PMEGP Subsidies</span>
                </Link>
              </li>
              <li>
                <Link href="/local-insights" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Hyper-Local Infrastructure GIS</span>
                </Link>
              </li>
              <li>
                <Link href="/reports" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Executive Bank Dossiers</span>
                </Link>
              </li>
              <li>
                <Link href="/profile" className="hover:text-brand-700 transition-colors flex items-center gap-1.5">
                  <span>Capability Calibration</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 4: Supported Govt Initiatives */}
          <div className="space-y-3">
            <h4 className="font-bold text-slate-900 uppercase text-[11px] tracking-wider">
              Supported Initiatives
            </h4>
            <div className="flex flex-wrap gap-1.5 text-[11px]">
              {["PM-VISHWAKARMA", "PMEGP", "PMFME", "Mudra Shishu", "DAY-NRLM", "Stand-Up India"].map(
                (scheme) => (
                  <span
                    key={scheme}
                    className="px-2 py-1 rounded-md bg-slate-100 text-slate-700 font-medium border border-slate-200/60"
                  >
                    {scheme}
                  </span>
                )
              )}
            </div>
            <p className="text-[11px] text-slate-400 pt-1">
              Ministry of Social Justice and Empowerment (MoSJE) • Government of India
            </p>
          </div>
        </div>

        {/* Bottom Copyright & Disclaimer */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-500">
          <div>
            © {currentYear} ThinkForge — Team ThinkForge (SIH26091). All rights reserved.
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              Engineered with <Heart className="w-3 h-3 text-red-500 fill-red-500 inline" /> for Rural India
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}

"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Compass,
  Users2,
  WalletCards,
  Landmark,
  MapPinned,
  FileSpreadsheet,
  UserCircle2,
  Sparkles,
  ShieldCheck,
  ChevronRight,
  X,
} from "lucide-react";
import clsx from "clsx";

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
}

const navItems: NavItem[] = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Opportunities", href: "/opportunities", icon: Compass, badge: "4 Viable" },
  { name: "Partners", href: "/partners", icon: Users2, badge: "7" },
  { name: "Finance", href: "/finance", icon: WalletCards },
  { name: "Schemes", href: "/schemes", icon: Landmark, badge: "PMEGP" },
  { name: "Local Insights", href: "/local-insights", icon: MapPinned },
  { name: "Reports", href: "/reports", icon: FileSpreadsheet },
  { name: "Profile", href: "/profile", icon: UserCircle2 },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen = false, onClose }) => {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-40 lg:hidden transition-opacity"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={clsx(
          "fixed top-0 bottom-0 left-0 z-50 w-72 bg-white border-r border-slate-200 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0",
          isOpen ? "translate-x-0 shadow-2xl" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Top Header & Brand */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <Link
            href="/dashboard"
            className="flex items-center gap-3 group focus:outline-none"
            onClick={onClose}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-600 to-emerald-700 flex items-center justify-center text-white shadow-glow-teal group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-emerald-200" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-slate-900 tracking-tight">
                  Think<span className="text-brand-600">Forge</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-widest px-1.5 py-0.5 rounded bg-brand-50 text-brand-700 border border-brand-200/60">
                  SIH91
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium leading-none mt-1">
                MoSJE Rural Advisory AI
              </p>
            </div>
          </Link>

          {/* Close button on mobile */}
          {onClose && (
            <button
              onClick={onClose}
              className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 focus:outline-none"
              aria-label="Close Sidebar"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Evidence Status Pill */}
        <div className="px-5 py-2.5 bg-slate-50/80 border-b border-slate-100 flex items-center justify-between text-xs">
          <span className="text-slate-500 font-medium flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-brand-600" />
            System Mode
          </span>
          <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full text-[11px] border border-emerald-200/80">
            Decision Cockpit
          </span>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto" aria-label="Main Navigation">
          <div className="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Platform Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive =
              pathname === item.href ||
              (item.href !== "/dashboard" && pathname?.startsWith(item.href));

            return (
              <Link
                key={item.name}
                href={item.href}
                onClick={onClose}
                className={clsx(
                  "flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group relative",
                  isActive
                    ? "bg-gradient-to-r from-brand-600 to-teal-700 text-white shadow-glow-teal font-semibold"
                    : "text-slate-600 hover:bg-slate-100/80 hover:text-slate-900"
                )}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    className={clsx(
                      "w-5 h-5 transition-colors",
                      isActive ? "text-emerald-200" : "text-slate-400 group-hover:text-brand-600"
                    )}
                  />
                  <span>{item.name}</span>
                </div>

                <div className="flex items-center gap-1.5">
                  {item.badge && (
                    <span
                      className={clsx(
                        "text-[10px] px-2 py-0.5 rounded-full font-semibold",
                        isActive
                          ? "bg-white/20 text-white"
                          : "bg-brand-50 text-brand-700 border border-brand-200"
                      )}
                    >
                      {item.badge}
                    </span>
                  )}
                  {isActive && <ChevronRight className="w-4 h-4 text-emerald-200" />}
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Active User Mini-Card */}
        <div className="p-3 border-t border-slate-200 bg-slate-50/70">
          <Link
            href="/profile"
            onClick={onClose}
            className="flex items-center gap-3 p-2.5 rounded-xl bg-white border border-slate-200/80 hover:border-brand-500 hover:shadow-sm transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-800 to-slate-950 text-emerald-400 font-bold flex items-center justify-center text-sm shadow-sm ring-2 ring-emerald-500/20">
              RK
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold text-slate-900 truncate">Ramesh Kumar</p>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              </div>
              <p className="text-[11px] text-slate-500 truncate">Wardha, MH • Agri-Cluster</p>
              <div className="mt-1 flex items-center gap-1.5">
                <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded border border-emerald-200">
                  Readiness: 78%
                </span>
              </div>
            </div>
          </Link>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

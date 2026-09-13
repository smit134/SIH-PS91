"use client";

import React, { useState } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Footer from "@/components/Footer";
import { Menu, Sparkles, UserCircle2, ArrowRight } from "lucide-react";
import Link from "next/link";
import { useLanguage } from "@/contexts/LanguageContext";

export default function ShellWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { t } = useLanguage();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // If on the registration or auth page, provide a focused shell without sidebar
  const isAuthPage = pathname === "/register" || pathname === "/auth";

  if (isAuthPage) {
    return (
      <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col selection:bg-brand-500 selection:text-white">
        {/* Focused Registration Header */}
        <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30 px-6 py-4 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-600 to-emerald-600 flex items-center justify-center text-white shadow-glow-teal">
              <Sparkles className="w-5 h-5 text-emerald-200" />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-tight">
                Think<span className="text-brand-400">Forge</span>
              </span>
              <span className="ml-2 text-[10px] font-bold uppercase tracking-wider bg-brand-950 text-brand-400 border border-brand-800/80 px-2 py-0.5 rounded">
                SIH26091
              </span>
            </div>
          </Link>

          <div className="flex items-center gap-3 text-sm">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-200 hover:bg-slate-700 hover:text-white border border-slate-700 transition-colors"
            >
              {t("shell_go_dashboard")}
              <ArrowRight className="w-3.5 h-3.5 text-brand-400" />
            </Link>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col">{children}</main>

        {/* Footer for Register Page */}
        <Footer dark />
      </div>
    );
  }

  if (isAuthPage) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-brand-500 selection:text-white">
        {/* Focused Auth Header */}
        <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30 px-6 py-4 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-600 to-emerald-600 flex items-center justify-center text-white shadow-glow-teal">
              <Sparkles className="w-5 h-5 text-emerald-200" />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-tight">
                Think<span className="text-brand-400">Forge</span>
              </span>
              <span className="ml-2 text-[10px] font-bold uppercase tracking-wider bg-brand-950 text-brand-400 border border-brand-800/80 px-2 py-0.5 rounded">
                SIH26091
              </span>
            </div>
          </Link>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-medium">Rural Enterprise Portal</span>
          </div>
        </header>

        {/* Auth Content */}
        <main className="flex-1 flex flex-col justify-center">{children}</main>

        {/* Footer for Auth Page */}
        <Footer dark />
      </div>
    );
  }

  // Dashboard & other authenticated/platform views
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col lg:flex-row antialiased">
      {/* Persistent Desktop & Mobile Drawer Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content Area */}
      <div className="flex-1 lg:pl-72 flex flex-col min-w-0">
        {/* Mobile Header Bar */}
        <header className="lg:hidden sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 py-3 flex items-center justify-between shadow-sm">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 -ml-1 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 focus:outline-none"
            aria-label="Open Navigation Menu"
          >
            <Menu className="w-6 h-6" />
          </button>

          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-brand-600 to-emerald-700 flex items-center justify-center text-white shadow-sm">
              <Sparkles className="w-4 h-4 text-emerald-100" />
            </div>
            <span className="font-bold text-slate-900">
              Think<span className="text-brand-600">Forge</span>
            </span>
          </Link>

          <Link
            href="/profile"
            className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 border border-slate-200"
            aria-label="User Profile"
          >
            <UserCircle2 className="w-5 h-5 text-slate-700" />
          </Link>
        </header>

        {/* Page Children */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>

        {/* Global Platform Footer */}
        <Footer />
      </div>
    </div>
  );
}

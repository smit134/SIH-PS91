"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  MapPin,
  Wrench,
  IndianRupee,
  Briefcase,
  Building2,
  ShieldAlert,
  ArrowRight,
  ArrowLeft,
  Sparkles,
  CheckCircle2,
  Lightbulb,
} from "lucide-react";
import clsx from "clsx";

interface FormData {
  // Step 1: Location
  state: string;
  district: string;
  block: string;
  mandiDistance: string;

  // Step 2: Skills
  primarySkill: string;
  experienceYears: string;
  isShgMember: boolean;

  // Step 3: Capital
  ownEquity: string;
  borrowingWillingness: string;
  hasCollateral: boolean;

  // Step 4: Business Interests
  sectorInterest: string;
  operatingModel: string;

  // Step 5: Resources
  landAccess: string;
  powerSupply: string;
  transportVehicle: string;

  // Step 6: Risk & Horizon
  riskAppetite: string;
  paybackExpectation: string;
}

const initialFormData: FormData = {
  state: "Maharashtra",
  district: "Wardha",
  block: "Deoli Gram Panchayat",
  mandiDistance: "14 km (Within APMC radius)",
  primarySkill: "Agri-Processing & Solar Operations",
  experienceYears: "4 - 7 Years",
  isShgMember: true,
  ownEquity: "₹1,50,000",
  borrowingWillingness: "₹2,00,000",
  hasCollateral: false,
  sectorInterest: "Post-Harvest Cold Chain & Food Value-Add",
  operatingModel: "Hybrid (Solo with SHG Tie-Up)",
  landAccess: "Owned Agricultural Shed (800 sq.ft)",
  powerSupply: "3-Phase Rural Grid (18 hrs/day)",
  transportVehicle: "Shared Auto-Trolley Access",
  riskAppetite: "Moderate (Capital Preserving with Steady Cashflow)",
  paybackExpectation: "12 - 18 Months",
};

const steps = [
  { id: 1, title: "Location", icon: MapPin, desc: "Geographic cluster & market access" },
  { id: 2, title: "Skills", icon: Wrench, desc: "Vocational expertise & history" },
  { id: 3, title: "Capital", icon: IndianRupee, desc: "Equity & borrowing willingness" },
  { id: 4, title: "Interests", icon: Briefcase, desc: "Preferred business sector" },
  { id: 5, title: "Resources", icon: Building2, desc: "Physical space, power & assets" },
  { id: 6, title: "Risk & Horizon", icon: ShieldAlert, desc: "Risk tolerance & timeline" },
];

export default function RegisterPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const updateField = <K extends keyof FormData>(key: K, value: FormData[K]) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleNext = () => {
    if (currentStep < 6) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      handleComplete();
    }
  };

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleComplete = () => {
    setIsSubmitting(true);
    try {
      if (typeof window !== "undefined") {
        localStorage.setItem("thinkforge_profile", JSON.stringify(formData));
      }
    } catch {
      // ignore storage err
    }

    setTimeout(() => {
      router.push("/dashboard");
    }, 600);
  };

  // Dynamic readiness estimate based on step progress
  const progressPercent = Math.round((currentStep / 6) * 100);

  return (
    <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-8 sm:py-12 flex flex-col justify-center">
      {/* Header Banner */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-950 border border-brand-800/80 text-brand-400 text-xs font-semibold mb-3">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>Smart Rural Onboarding Wizard</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Entrepreneur Capability Profile
        </h1>
        <p className="mt-2 text-sm text-slate-400 max-w-xl mx-auto">
          ThinkForge uses your grounded inputs to evaluate localized feasibility, match schemes, and synthesize a bankable roadmap.
        </p>
      </div>

      {/* Stepper Progress Bar */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-2xl p-4 sm:p-6 mb-8 shadow-xl">
        <div className="flex items-center justify-between text-xs font-semibold mb-3">
          <span className="text-slate-400">
            Step <span className="text-brand-400 font-bold">{currentStep}</span> of 6:{" "}
            <span className="text-white">{steps[currentStep - 1].title}</span>
          </span>
          <span className="text-emerald-400 font-mono">{progressPercent}% Completed</span>
        </div>

        {/* Progress Bar Track */}
        <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden mb-6">
          <div
            className="h-full bg-gradient-to-r from-brand-500 to-emerald-400 transition-all duration-500 ease-out rounded-full shadow-glow-teal"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Step Icons Pill Navigation */}
        <div className="grid grid-cols-6 gap-2 sm:gap-3">
          {steps.map((s) => {
            const Icon = s.icon;
            const isDone = currentStep > s.id;
            const isCurrent = currentStep === s.id;

            return (
              <button
                key={s.id}
                type="button"
                onClick={() => setCurrentStep(s.id)}
                className={clsx(
                  "flex flex-col items-center gap-1.5 py-2 px-1 rounded-xl text-center transition-all focus:outline-none",
                  isCurrent
                    ? "bg-brand-600/20 border border-brand-500 text-brand-300 ring-1 ring-brand-500/50"
                    : isDone
                    ? "bg-slate-900 border border-slate-800 text-emerald-400 hover:border-slate-700"
                    : "bg-slate-900/40 border border-slate-800/50 text-slate-500 hover:text-slate-400"
                )}
              >
                <div
                  className={clsx(
                    "w-7 h-7 rounded-lg flex items-center justify-center transition-colors",
                    isCurrent
                      ? "bg-brand-500 text-slate-950 font-bold"
                      : isDone
                      ? "bg-emerald-950 text-emerald-300"
                      : "bg-slate-800 text-slate-500"
                  )}
                >
                  {isDone ? <CheckCircle2 className="w-4 h-4" /> : <Icon className="w-4 h-4" />}
                </div>
                <span className="text-[10px] font-semibold truncate hidden sm:block">
                  {s.title}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Interactive Form Card */}
      <div className="bg-slate-950 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        {/* Step 1: Location */}
        {currentStep === 1 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <MapPin className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Geographic & Rural Cluster</h3>
                <p className="text-xs text-slate-400">
                  Where will your business operate? Helps calculate local demand & APMC mandi distance.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">State</label>
                <input
                  type="text"
                  value={formData.state}
                  onChange={(e) => updateField("state", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">District</label>
                <input
                  type="text"
                  value={formData.district}
                  onChange={(e) => updateField("district", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Block / Gram Panchayat
                </label>
                <input
                  type="text"
                  value={formData.block}
                  onChange={(e) => updateField("block", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Distance to Primary Mandi / Town
                </label>
                <select
                  value={formData.mandiDistance}
                  onChange={(e) => updateField("mandiDistance", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Under 5 km (Immediate Mandi Access)</option>
                  <option>5 - 15 km (Semi-Peripheral)</option>
                  <option>15 - 30 km (Rural Deep)</option>
                  <option>Above 30 km (Remote Outlier)</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Skills */}
        {currentStep === 2 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <Wrench className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Skills & Production Capacity</h3>
                <p className="text-xs text-slate-400">
                  Your primary craft or technical knowledge to determine operational feasibility.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Primary Vocational Skill
                </label>
                <select
                  value={formData.primarySkill}
                  onChange={(e) => updateField("primarySkill", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Agri-Processing & Solar Operations</option>
                  <option>Food Preservation & Pickling/Pulses</option>
                  <option>Electrical, Solar & Pump Repair</option>
                  <option>Dairy Chilling & Milk Aggregation</option>
                  <option>Handloom & Natural Fiber Weaving</option>
                  <option>Mechanical Fabrication & Metalwork</option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">
                    Years of Practical Experience
                  </label>
                  <select
                    value={formData.experienceYears}
                    onChange={(e) => updateField("experienceYears", e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                  >
                    <option>Beginner (0 - 1 Year)</option>
                    <option>1 - 3 Years</option>
                    <option>4 - 7 Years</option>
                    <option>8+ Years (Master Practitioner)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">
                    Self-Help Group (SHG) / FPO Affiliation
                  </label>
                  <div className="flex gap-3 pt-1">
                    <button
                      type="button"
                      onClick={() => updateField("isShgMember", true)}
                      className={clsx(
                        "flex-1 py-2 px-3 rounded-xl text-xs font-semibold border transition-colors",
                        formData.isShgMember
                          ? "bg-brand-600 border-brand-500 text-white"
                          : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
                      )}
                    >
                      Yes, Active Member
                    </button>
                    <button
                      type="button"
                      onClick={() => updateField("isShgMember", false)}
                      className={clsx(
                        "flex-1 py-2 px-3 rounded-xl text-xs font-semibold border transition-colors",
                        !formData.isShgMember
                          ? "bg-brand-600 border-brand-500 text-white"
                          : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
                      )}
                    >
                      No Affiliation
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Capital */}
        {currentStep === 3 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <IndianRupee className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Capital & Financial Capacity</h3>
                <p className="text-xs text-slate-400">
                  Your available equity and debt appetite to structure your project cost and loan ratio.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Available Personal Savings / Equity
                </label>
                <select
                  value={formData.ownEquity}
                  onChange={(e) => updateField("ownEquity", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>₹50,000 (Micro Bootstrap)</option>
                  <option>₹1,00,000</option>
                  <option>₹1,50,000</option>
                  <option>₹2,50,000</option>
                  <option>₹5,00,000+</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Comfortable Loan / Borrowing Limit
                </label>
                <select
                  value={formData.borrowingWillingness}
                  onChange={(e) => updateField("borrowingWillingness", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>₹1,00,000 (Low Debt Burden)</option>
                  <option>₹2,00,000</option>
                  <option>₹3,50,000 (PMEGP Band)</option>
                  <option>₹5,00,000+</option>
                </select>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-white">Collateral Security Available?</p>
                <p className="text-[11px] text-slate-400">
                  Land deed, fixed deposit, or vehicle hypothecation
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => updateField("hasCollateral", true)}
                  className={clsx(
                    "px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors",
                    formData.hasCollateral
                      ? "bg-brand-600 text-white border-brand-500"
                      : "bg-slate-800 text-slate-400 border-slate-700"
                  )}
                >
                  Yes
                </button>
                <button
                  type="button"
                  onClick={() => updateField("hasCollateral", false)}
                  className={clsx(
                    "px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors",
                    !formData.hasCollateral
                      ? "bg-brand-600 text-white border-brand-500"
                      : "bg-slate-800 text-slate-400 border-slate-700"
                  )}
                >
                  No (Mudra / CGTMSE)
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Business Interests */}
        {currentStep === 4 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <Briefcase className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Business Interests & Sector</h3>
                <p className="text-xs text-slate-400">
                  What kind of enterprise are you passionate about building?
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Target Sector Focus
                </label>
                <select
                  value={formData.sectorInterest}
                  onChange={(e) => updateField("sectorInterest", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Post-Harvest Cold Chain & Food Value-Add</option>
                  <option>Bio-Waste Briquette & Renewable Energy</option>
                  <option>Dairy Value Added Products (Ghee, Paneer)</option>
                  <option>Agro-Textile & Natural Fiber Extraction</option>
                  <option>Rural Last-Mile Logistics & Hub</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Preferred Operating Model
                </label>
                <select
                  value={formData.operatingModel}
                  onChange={(e) => updateField("operatingModel", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Hybrid (Solo with SHG Tie-Up)</option>
                  <option>Individual Sole Proprietorship</option>
                  <option>Co-operative / FPO Joint Venture</option>
                  <option>Family Partnership Unit</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Step 5: Resources */}
        {currentStep === 5 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Physical Assets & Utilities</h3>
                <p className="text-xs text-slate-400">
                  Existing infrastructure reduces initial setup costs and shortens break-even.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Land / Commercial Shed Availability
                </label>
                <select
                  value={formData.landAccess}
                  onChange={(e) => updateField("landAccess", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Owned Agricultural Shed (800 sq.ft)</option>
                  <option>Open Land Plot (Need to Erect Shed)</option>
                  <option>Rented Village Facility</option>
                  <option>No Land (Need Common Facility Center)</option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">
                    Electricity Grid Status
                  </label>
                  <select
                    value={formData.powerSupply}
                    onChange={(e) => updateField("powerSupply", e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                  >
                    <option>3-Phase Rural Grid (18 hrs/day)</option>
                    <option>Single-Phase Domestic Connection</option>
                    <option>Solar Hybrid Feeder Available</option>
                    <option>Frequent Outages / Off-Grid</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">
                    Transport Vehicle Access
                  </label>
                  <select
                    value={formData.transportVehicle}
                    onChange={(e) => updateField("transportVehicle", e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                  >
                    <option>Shared Auto-Trolley Access</option>
                    <option>Own Mini-Pickup Truck</option>
                    <option>Motorcycle / Moped Only</option>
                    <option>Rely on Third-Party Logistics</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 6: Risk & Horizon */}
        {currentStep === 6 && (
          <div className="space-y-5 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center border border-brand-500/20">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Risk Appetite & Target Timeline</h3>
                <p className="text-xs text-slate-400">
                  Calibrate your risk profile to protect your household income during startup phases.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Risk Tolerance Profile
                </label>
                <select
                  value={formData.riskAppetite}
                  onChange={(e) => updateField("riskAppetite", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>Moderate (Capital Preserving with Steady Cashflow)</option>
                  <option>Conservative (Minimal Debt, Subsidy-Anchored)</option>
                  <option>Aggressive / Growth-Oriented (High Scale)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Target Break-Even Horizon
                </label>
                <select
                  value={formData.paybackExpectation}
                  onChange={(e) => updateField("paybackExpectation", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option>6 - 12 Months (Fast Cash Recovery)</option>
                  <option>12 - 18 Months (Standard Agro-Cycle)</option>
                  <option>18 - 24 Months (Asset Heavy)</option>
                </select>
              </div>

              {/* Ready summary */}
              <div className="p-4 rounded-xl bg-brand-950/60 border border-brand-800/80 flex items-start gap-3 text-xs text-slate-300">
                <Lightbulb className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-white block mb-0.5">
                    Profile Synthesis Ready:
                  </span>
                  Your profile matches 4 verified local opportunities in Wardha with 95% PMEGP subsidy eligibility!
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-8 pt-5 border-t border-slate-800 flex items-center justify-between gap-4">
          {currentStep > 1 ? (
            <button
              type="button"
              onClick={handlePrev}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-slate-900 text-slate-300 hover:bg-slate-800 hover:text-white border border-slate-700 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Previous Step
            </button>
          ) : (
            <div />
          )}

          {currentStep < 6 ? (
            <button
              type="button"
              onClick={handleNext}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-bold bg-brand-600 text-white hover:bg-brand-500 shadow-glow-teal transition-all"
            >
              <span>Continue to {steps[currentStep].title}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleComplete}
              disabled={isSubmitting}
              className="inline-flex items-center gap-2 px-7 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-brand-500 via-emerald-600 to-teal-600 text-white hover:opacity-95 shadow-glow-emerald transition-all transform hover:scale-[1.02] active:scale-[0.98]"
            >
              <Sparkles className="w-4 h-4 text-emerald-100" />
              <span>{isSubmitting ? "Synthesizing Roadmap..." : "Complete & Launch Dashboard"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

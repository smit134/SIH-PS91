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
  // Step 1: Location & Profile
  name: string;
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

const locationData: Record<string, Record<string, string[]>> = {
  Maharashtra: {
    Wardha: ["Deoli Gram Panchayat", "Seloo", "Hinganghat", "Arvi"],
    Nagpur: ["Kamptee", "Hingna", "Katol"],
    Pune: ["Haveli", "Khed", "Maval"],
    Nashik: ["Malegaon", "Sinnar", "Igatpuri"]
  },
  Gujarat: {
    Ahmedabad: ["Sanand", "Daskroi", "Bavla"],
    Surat: ["Olpad", "Mangrol", "Mandvi"]
  },
  Karnataka: {
    Bengaluru: ["Anekal", "Yelahanka", "Kengeri"],
    Mysuru: ["Hunsur", "Nanjangud", "T Narsipur"]
  },
  "Madhya Pradesh": {
    Indore: ["Mhow", "Sanwer", "Depalpur"],
    Bhopal: ["Huzur", "Berasia"]
  }
};

const initialFormData: FormData = {
  name: "",
  state: "",
  district: "",
  block: "",
  mandiDistance: "",
  primarySkill: "",
  experienceYears: "",
  isShgMember: false,
  ownEquity: "",
  borrowingWillingness: "",
  hasCollateral: false,
  sectorInterest: "",
  operatingModel: "",
  landAccess: "",
  powerSupply: "",
  transportVehicle: "",
  riskAppetite: "",
  paybackExpectation: "",
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

  const handleComplete = async () => {
    setIsSubmitting(true);
    try {
      if (typeof window !== "undefined") {
        localStorage.setItem("thinkforge_profile", JSON.stringify(formData));
        if (formData.name) {
          localStorage.setItem("thinkforge_name", formData.name);
        }
        
        const userId = localStorage.getItem("thinkforge_token");
        if (userId) {
          await fetch(`http://localhost:8000/users/${userId}/profile`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
          });
        }
        
        window.dispatchEvent(new Event("profileUpdated"));
      }
    } catch (err) {
      console.error("Failed to save profile", err);
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
              <div className="sm:col-span-2">
                <label className="block text-xs font-medium text-slate-300 mb-1.5">Full Name</label>
                <input
                  type="text"
                  placeholder="Enter your name"
                  value={formData.name}
                  onChange={(e) => updateField("name", e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">State</label>
                <select
                  value={formData.state}
                  onChange={(e) => {
                    updateField("state", e.target.value);
                    updateField("district", "");
                    updateField("block", "");
                  }}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none"
                >
                  <option value="">Select State...</option>
                  {Object.keys(locationData).map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">District</label>
                <select
                  value={formData.district}
                  onChange={(e) => {
                    updateField("district", e.target.value);
                    updateField("block", "");
                  }}
                  disabled={!formData.state}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none disabled:opacity-50"
                >
                  <option value="">Select District...</option>
                  {formData.state && locationData[formData.state] && Object.keys(locationData[formData.state]).map(district => (
                    <option key={district} value={district}>{district}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Block / Gram Panchayat
                </label>
                <select
                  value={formData.block}
                  onChange={(e) => updateField("block", e.target.value)}
                  disabled={!formData.district}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none disabled:opacity-50"
                >
                  <option value="">Select Block...</option>
                  {formData.state && formData.district && locationData[formData.state]?.[formData.district]?.map(block => (
                    <option key={block} value={block}>{block}</option>
                  ))}
                </select>
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
                  <option value="">Select Distance...</option>
                  <option value="Under 5 km (Immediate Mandi Access)">Under 5 km (Immediate Mandi Access)</option>
                  <option value="5 - 15 km (Semi-Peripheral)">5 - 15 km (Semi-Peripheral)</option>
                  <option value="15 - 30 km (Rural Deep)">15 - 30 km (Rural Deep)</option>
                  <option value="Above 30 km (Remote Outlier)">Above 30 km (Remote Outlier)</option>
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
                  <option value="">Select Skill...</option>
                  <option value="Agri-Processing & Solar Operations">Agri-Processing & Solar Operations</option>
                  <option value="Food Preservation & Pickling/Pulses">Food Preservation & Pickling/Pulses</option>
                  <option value="Electrical, Solar & Pump Repair">Electrical, Solar & Pump Repair</option>
                  <option value="Dairy Chilling & Milk Aggregation">Dairy Chilling & Milk Aggregation</option>
                  <option value="Handloom & Natural Fiber Weaving">Handloom & Natural Fiber Weaving</option>
                  <option value="Mechanical Fabrication & Metalwork">Mechanical Fabrication & Metalwork</option>
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
                    <option value="">Select Experience...</option>
                    <option value="Beginner (0 - 1 Year)">Beginner (0 - 1 Year)</option>
                    <option value="1 - 3 Years">1 - 3 Years</option>
                    <option value="4 - 7 Years">4 - 7 Years</option>
                    <option value="8+ Years (Master Practitioner)">8+ Years (Master Practitioner)</option>
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
                  <option value="">Select Amount...</option>
                  <option value="₹50,000 (Micro Bootstrap)">₹50,000 (Micro Bootstrap)</option>
                  <option value="₹1,00,000">₹1,00,000</option>
                  <option value="₹1,50,000">₹1,50,000</option>
                  <option value="₹2,50,000">₹2,50,000</option>
                  <option value="₹5,00,000+">₹5,00,000+</option>
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
                  <option value="">Select Amount...</option>
                  <option value="₹1,00,000 (Low Debt Burden)">₹1,00,000 (Low Debt Burden)</option>
                  <option value="₹2,00,000">₹2,00,000</option>
                  <option value="₹3,50,000 (PMEGP Band)">₹3,50,000 (PMEGP Band)</option>
                  <option value="₹5,00,000+">₹5,00,000+</option>
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
                  <option value="">Select Sector...</option>
                  <option value="Post-Harvest Cold Chain & Food Value-Add">Post-Harvest Cold Chain & Food Value-Add</option>
                  <option value="Bio-Waste Briquette & Renewable Energy">Bio-Waste Briquette & Renewable Energy</option>
                  <option value="Dairy Value Added Products (Ghee, Paneer)">Dairy Value Added Products (Ghee, Paneer)</option>
                  <option value="Agro-Textile & Natural Fiber Extraction">Agro-Textile & Natural Fiber Extraction</option>
                  <option value="Rural Last-Mile Logistics & Hub">Rural Last-Mile Logistics & Hub</option>
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
                  <option value="">Select Model...</option>
                  <option value="Hybrid (Solo with SHG Tie-Up)">Hybrid (Solo with SHG Tie-Up)</option>
                  <option value="Individual Sole Proprietorship">Individual Sole Proprietorship</option>
                  <option value="Co-operative / FPO Joint Venture">Co-operative / FPO Joint Venture</option>
                  <option value="Family Partnership Unit">Family Partnership Unit</option>
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
                  <option value="">Select Land Access...</option>
                  <option value="Owned Agricultural Shed (800 sq.ft)">Owned Agricultural Shed (800 sq.ft)</option>
                  <option value="Open Land Plot (Need to Erect Shed)">Open Land Plot (Need to Erect Shed)</option>
                  <option value="Rented Village Facility">Rented Village Facility</option>
                  <option value="No Land (Need Common Facility Center)">No Land (Need Common Facility Center)</option>
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
                    <option value="">Select Power Status...</option>
                    <option value="3-Phase Rural Grid (18 hrs/day)">3-Phase Rural Grid (18 hrs/day)</option>
                    <option value="Single-Phase Domestic Connection">Single-Phase Domestic Connection</option>
                    <option value="Solar Hybrid Feeder Available">Solar Hybrid Feeder Available</option>
                    <option value="Frequent Outages / Off-Grid">Frequent Outages / Off-Grid</option>
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
                    <option value="">Select Transport...</option>
                    <option value="Shared Auto-Trolley Access">Shared Auto-Trolley Access</option>
                    <option value="Own Mini-Pickup Truck">Own Mini-Pickup Truck</option>
                    <option value="Motorcycle / Moped Only">Motorcycle / Moped Only</option>
                    <option value="Rely on Third-Party Logistics">Rely on Third-Party Logistics</option>
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
                  <option value="">Select Risk Profile...</option>
                  <option value="Moderate (Capital Preserving with Steady Cashflow)">Moderate (Capital Preserving with Steady Cashflow)</option>
                  <option value="Conservative (Minimal Debt, Subsidy-Anchored)">Conservative (Minimal Debt, Subsidy-Anchored)</option>
                  <option value="Aggressive / Growth-Oriented (High Scale)">Aggressive / Growth-Oriented (High Scale)</option>
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
                  <option value="">Select Horizon...</option>
                  <option value="6 - 12 Months (Fast Cash Recovery)">6 - 12 Months (Fast Cash Recovery)</option>
                  <option value="12 - 18 Months (Standard Agro-Cycle)">12 - 18 Months (Standard Agro-Cycle)</option>
                  <option value="18 - 24 Months (Asset Heavy)">18 - 24 Months (Asset Heavy)</option>
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

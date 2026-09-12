"use client";

import React, { useState, useEffect } from "react";
import EvidenceBadge from "@/components/EvidenceBadge";
import { MapPin, Handshake, ShieldCheck, PhoneCall, Loader2 } from "lucide-react";

export default function PartnersPage() {
  const [partners, setPartners] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [introRequested, setIntroRequested] = useState(false);

  useEffect(() => {
    const fetchPartners = async () => {
      try {
        const storedProfile = localStorage.getItem("thinkforge_profile");
        const rawProfile = storedProfile ? JSON.parse(storedProfile) : {};
        
        // Map UI profile format to Backend EntrepreneurProfile schema
        const profile = {
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

        const res = await fetch("http://localhost:8000/api/intelligence/partner/recommendations?max_radius_km=50", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(profile)
        });

        if (res.ok) {
          const data = await res.json();
          setPartners(data);
        } else {
          console.error("Failed to fetch partners");
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchPartners();
  }, []);

  const handleConnect = async (partnerId: string, idx: number) => {
    try {
      const storedToken = localStorage.getItem("thinkforge_token") || "demo_user";
      const res = await fetch("http://localhost:8000/api/intelligence/partner/request-contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ partner_id: partnerId, user_id: storedToken })
      });
      if (res.ok) {
        const contactData = await res.json();
        setPartners(prev => {
          const updated = [...prev];
          updated[idx] = {
            ...updated[idx],
            is_contact_shared: true,
            contact_phone: contactData.phone
          };
          return updated;
        });
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <Handshake className="w-4 h-4 text-brand-600" />
            <span>PARTNER ECOSYSTEM</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Capability Complementarity</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Matched Local Partners</h1>
          <p className="text-sm text-slate-600">
            Discover verified FPOs, SHGs, and logistics providers that bridge your equipment, space, or market access gaps.
          </p>
        </div>

        <button 
          onClick={() => setIntroRequested(true)}
          disabled={introRequested}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all shadow-glow-teal ${
            introRequested 
              ? "bg-emerald-600 text-white cursor-default" 
              : "bg-brand-600 text-white hover:bg-brand-700"
          }`}
        >
          {introRequested ? (
            <>
              <ShieldCheck className="w-4 h-4 text-emerald-200" />
              Introductions Requested
            </>
          ) : (
            <>
              <Handshake className="w-4 h-4 text-emerald-200" />
              Request Partner Introduction
            </>
          )}
        </button>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500 mb-4" />
          <p>Scanning ecosystem for complementary partners...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {partners.map((partner, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card hover:shadow-card-elevated transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <EvidenceBadge type={partner.verification_state || "VERIFIED"} />
                  <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    Synergy {Math.round(partner.synergy_score || 90)}%
                  </span>
                </div>

                <h3 className="font-bold text-base text-slate-900 mt-2">{partner.display_title || partner.name}</h3>
                <p className="text-xs font-semibold text-brand-700 mt-0.5">{partner.investment_range_str || partner.type}</p>

                <div className="mt-3 space-y-1.5 text-xs text-slate-600">
                  <div className="flex items-center gap-1.5 text-slate-500">
                    <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span>{partner.approximate_area || partner.location}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-500">
                    <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span>Strengths: {partner.key_strengths?.join(", ") || partner.members}</span>
                  </div>
                </div>

                <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                    Capability Synergy
                  </p>
                  <p className="text-xs text-slate-700 mt-1 font-medium leading-relaxed">
                    {partner.why_matched?.[0] || partner.complementaryFit || "Complementary resource sharing."}
                  </p>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-400 font-medium">Verified by District MSME</span>
                {partner.is_contact_shared ? (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-lg text-xs font-bold border border-emerald-200 shadow-sm">
                    <PhoneCall className="w-3.5 h-3.5" />
                    {partner.contact_phone}
                  </span>
                ) : (
                  <button 
                    onClick={() => handleConnect(partner.partner_id, idx)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-brand-50 text-brand-700 hover:bg-brand-100 rounded-lg text-xs font-bold transition-colors"
                  >
                    <Handshake className="w-3.5 h-3.5" />
                    Connect
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

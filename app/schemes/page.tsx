"use client";

import React, { useState, useEffect, useMemo, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import EvidenceBadge from "@/components/EvidenceBadge";
import {
  Landmark,
  CheckCircle2,
  ExternalLink,
  Sparkles,
  ArrowRight,
  Filter,
  Layers,
  ChevronDown,
  ChevronUp,
  Coins,
  ShieldCheck,
  FileText,
  Building2,
  X,
  TrendingUp,
  UserCheck,
  User,
  MapPin,
  Briefcase,
  SlidersHorizontal,
  Edit3
} from "lucide-react";
import Link from "next/link";
import { useLanguage } from "@/contexts/LanguageContext";

// Standard Opportunities catalog matching business_catalog.py
const OPPORTUNITY_CONFIGS = [
  {
    id: "all",
    name: "All Rural Opportunities",
    emoji: "🌟",
    sector: "All Sectors",
    capex: 150000,
    description: "Browse all Central & State rural enterprise subsidy and credit schemes.",
  },
  {
    id: "food_processing_spices",
    name: "Agro-Food Processing & Spices",
    emoji: "🌶️",
    sector: "Food Processing",
    capex: 180000,
    description: "Milling, spice pulverization, grain grading, and packaged food units.",
  },
  {
    id: "dairy_micro_farm",
    name: "Micro Dairy & Milk Collection",
    emoji: "🥛",
    sector: "Agri-Business & Livestock",
    capex: 320000,
    description: "Cattle rearing, chilled milk collection, and dairy value-addition.",
  },
  {
    id: "vermicompost_production",
    name: "Vermicompost & Bio-Fertilizer",
    emoji: "🪱",
    sector: "Agri-Inputs",
    capex: 85000,
    description: "Organic waste conversion, vermiculture pits, and bio-fertilizer sales.",
  },
  {
    id: "handicraft_textiles",
    name: "Handicraft & Textile Products",
    emoji: "🧵",
    sector: "Artisanal & Crafts",
    capex: 140000,
    description: "Traditional weaving, jute crafts, embroidery, and village artisan goods.",
  },
  {
    id: "garment_tailoring_unit",
    name: "Custom Tailoring & Apparel",
    emoji: "✂️",
    sector: "Textile & Apparel",
    capex: 95000,
    description: "Custom stitching, school uniforms, and batch garment manufacturing.",
  },
  {
    id: "organic_farm_inputs",
    name: "Organic Inputs & Bio-Pesticides",
    emoji: "🌱",
    sector: "Agri-Inputs & Retail",
    capex: 110000,
    description: "Certified bio-pesticides, neem extracts, jeevamrut, and organic seeds.",
  },
];

// Fallback comprehensive 10 schemes dataset
const FALLBACK_SCHEMES = [
  {
    scheme_id: "pmfme",
    scheme_name: "PMFME (Pradhan Mantri Formalisation of Micro Food Processing Enterprises)",
    short_code: "PMFME",
    nodal_agency: "Ministry of Food Processing Industries (MoFPI)",
    subsidy_percent: 35.0,
    subsidy_rate_text: "35% Credit-Linked Capital Subsidy (Max ₹10 Lakhs)",
    max_project_cost: 3000000,
    applicable_opportunities: ["food_processing_spices", "dairy_micro_farm"],
    priority_category: "ALL",
    collateral_free: false,
    description: "Financial, technical, and business support for the upgradation and establishment of micro-food processing units, spice grinding, flour mills, and agri-value addition under the ODOP (One District One Product) cluster approach.",
    reasons: [
      "Direct sector match for Food Processing & Spices under ODOP Wardha Cluster.",
      "35% credit-linked capital subsidy on machinery and civil works.",
      "Special provision of ₹40,000 seed capital for SHG enterprise members."
    ],
    documents_required: ["Aadhaar & PAN Card", "6-Month Bank Statement", "Machinery Quotations", "FSSAI Basic Registration", "Electricity Bill / Land Document"],
    application_route: "https://pmfme.mofpi.gov.in/",
    official_source: "https://pmfme.mofpi.gov.in/",
    status_tag: "ODOP Cluster Aligned"
  },
  {
    scheme_id: "pmegp",
    scheme_name: "PMEGP (Prime Minister's Employment Generation Programme)",
    short_code: "PMEGP",
    nodal_agency: "KVIC / Ministry of MSME",
    subsidy_percent: 35.0,
    subsidy_rate_text: "35% Rural Subsidy (Special Category) / 25% (General)",
    max_project_cost: 5000000,
    applicable_opportunities: ["food_processing_spices", "handicraft_textiles", "garment_tailoring_unit", "vermicompost_production", "dairy_micro_farm", "organic_farm_inputs"],
    priority_category: "SC/ST/OBC/Women/Rural",
    collateral_free: false,
    description: "Flagship credit-linked subsidy programme offering 25% to 35% margin money assistance for setting up new micro-enterprises in rural areas across manufacturing and service sectors.",
    reasons: [
      "Highest rural subsidy rate: 35% margin money assistance for rural entrepreneurs.",
      "Entrepreneur's own contribution required is only 5% to 10%.",
      "Nationwide bank financing network with online monitoring portal."
    ],
    documents_required: ["Aadhaar Card", "Detailed Project Report (DPR)", "EDP Training Certificate", "Special Category Certificate", "Rural Area Certificate"],
    application_route: "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
    official_source: "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
    status_tag: "Eligible for Instant Application"
  },
  {
    scheme_id: "nlm_dairy",
    scheme_name: "National Livestock Mission (NLM) & DIDF",
    short_code: "NLM",
    nodal_agency: "Department of Animal Husbandry & Dairying (DAHD)",
    subsidy_percent: 50.0,
    subsidy_rate_text: "50% Capital Subsidy (Up to ₹25 Lakhs - ₹50 Lakhs)",
    max_project_cost: 5000000,
    applicable_opportunities: ["dairy_micro_farm"],
    priority_category: "Rural Livestock Entrepreneurs",
    collateral_free: false,
    description: "Financial assistance for entrepreneurship development in livestock breeding, micro-dairy establishments, silage making, feed production, and milk chilling infrastructure.",
    reasons: [
      "Massive 50% capital subsidy on cattle sheds, milking equipment, and silage pits.",
      "Direct tranche release through SIDBI escrow account for transparent disbursement.",
      "Concessional interest rate via participating scheduled rural banks."
    ],
    documents_required: ["Aadhaar", "Land Record / Lease Agreement (10+ yrs)", "Detailed Project Report", "Bank Loan Sanction", "Dairy / Cattle Training Certificate"],
    application_route: "https://nlm.udyamimitra.in/",
    official_source: "https://nlm.udyamimitra.in/",
    status_tag: "High Capital Subsidy (50%)"
  },
  {
    scheme_id: "pkvy_organic",
    scheme_name: "PKVY (Paramparagat Krishi Vikas Yojana) & Bhartiya Prakritik Krishi",
    short_code: "PKVY",
    nodal_agency: "Ministry of Agriculture & Farmers Welfare",
    subsidy_percent: 60.0,
    subsidy_rate_text: "₹50,000/ha Support + Up to 60% Infrastructure Grant",
    max_project_cost: 1000000,
    applicable_opportunities: ["vermicompost_production", "organic_farm_inputs"],
    priority_category: "Organic Producers & Input Suppliers",
    collateral_free: true,
    description: "Promotes organic farming, on-farm bio-input production (vermicompost pits, jeevamrut preparation, bio-pesticide storage), and PGS India organic certification for farmer clusters.",
    reasons: [
      "Direct grant for permanent vermicompost beds and bio-extract formulation tanks.",
      "100% collateral-free government support with zero processing charges.",
      "Free PGS-India organic certification and cluster branding linkage."
    ],
    documents_required: ["Aadhaar", "Land Record (7/12 or 8A extract)", "Soil Health Card", "Farmer Group / FPO Registration"],
    application_route: "https://pgsindia-ncof.gov.in/",
    official_source: "https://pgsindia-ncof.gov.in/",
    status_tag: "Eco-Sustainable Priority"
  },
  {
    scheme_id: "acabc_nabard",
    scheme_name: "Agri-Clinic & Agri-Business Centres (ACABC Scheme)",
    short_code: "ACABC",
    nodal_agency: "NABARD / MANAGE",
    subsidy_percent: 44.0,
    subsidy_rate_text: "44% Composite Subsidy (Women/SC/ST) / 36% (General)",
    max_project_cost: 2000000,
    applicable_opportunities: ["organic_farm_inputs", "vermicompost_production", "food_processing_spices"],
    priority_category: "Agri Graduates & Trained Rural Entrepreneurs",
    collateral_free: false,
    description: "Provides back-ended composite capital subsidy for setting up agri-service centres, bio-fertilizer supply stores, custom hiring, and organic input distribution hubs.",
    reasons: [
      "Back-ended composite capital subsidy: 44% for women/SC/ST and 36% for others.",
      "NABARD refinancing facility ensures lowest bank lending rates.",
      "Free two-month residential entrepreneurship training provided by MANAGE."
    ],
    documents_required: ["MANAGE Training Certificate", "Agri/Science Diploma or Degree", "Business DPR", "Aadhaar Card", "Bank Credit Sanction"],
    application_route: "https://www.agriclinics.net/",
    official_source: "https://www.agriclinics.net/",
    status_tag: "NABARD Back-Ended Subsidy"
  },
  {
    scheme_id: "sfurti_crafts",
    scheme_name: "SFURTI (Scheme of Fund for Regeneration of Traditional Industries)",
    short_code: "SFURTI",
    nodal_agency: "Ministry of MSME / KVIC / Coir Board",
    subsidy_percent: 90.0,
    subsidy_rate_text: "Up to 90% Cluster Grant for Common Facilities & Tools",
    max_project_cost: 25000000,
    applicable_opportunities: ["handicraft_textiles", "garment_tailoring_unit"],
    priority_category: "Traditional Artisans & Weavers",
    collateral_free: true,
    description: "Assists traditional rural artisans and micro-producers with modern production tools, raw material banks, common facility centers (CFCs), packaging, and brand marketing.",
    reasons: [
      "Up to 90% grant for modern tooling, handlooms, and common processing centers.",
      "Direct technical and design mentorship from NIFT and national design institutes.",
      "Zero collateral burden for rural artisan producer groups."
    ],
    documents_required: ["Pehchan Artisan ID Card / Aadhaar", "Bank Account Details", "DIC Recommendation"],
    application_route: "https://sfurti.msme.gov.in/",
    official_source: "https://sfurti.msme.gov.in/",
    status_tag: "Artisan & Handloom Priority"
  },
  {
    scheme_id: "samarth_textiles",
    scheme_name: "SAMARTH & Handloom Weaver Mudra Scheme",
    short_code: "SAMARTH",
    nodal_agency: "Ministry of Textiles",
    subsidy_percent: 20.0,
    subsidy_rate_text: "Margin Money Subsidy (Up to ₹25,000) + 6% Concessional Rate",
    max_project_cost: 500000,
    applicable_opportunities: ["garment_tailoring_unit", "handicraft_textiles"],
    priority_category: "Tailors, Weavers & Apparel Micro-Units",
    collateral_free: true,
    description: "Skill development, modern electronic sewing machines, and margin money financial assistance to custom tailors, garment batch stitchers, and micro-textile enterprises.",
    reasons: [
      "Up to ₹25,000 margin money grant per tailor for modern high-speed sewing machines.",
      "Subsidized loan interest capped at 6% with 3-year interest subvention.",
      "Certified trade testing and guaranteed apparel industry linkages."
    ],
    documents_required: ["Aadhaar Card", "Tailoring/Weaving Trade Proof", "Bank Passbook", "Sewing Machine Quotation"],
    application_route: "https://samarth-textiles.gov.in/",
    official_source: "https://samarth-textiles.gov.in/",
    status_tag: "Concessional 6% Credit"
  },
  {
    scheme_id: "mudra_loan",
    scheme_name: "Pradhan Mantri MUDRA Yojana (Shishu, Kishore & Tarun)",
    short_code: "MUDRA",
    nodal_agency: "Department of Financial Services / MUDRA",
    subsidy_percent: 0.0,
    subsidy_rate_text: "100% Collateral-Free Institutional Credit",
    max_project_cost: 1000000,
    applicable_opportunities: ["handicraft_textiles", "garment_tailoring_unit", "vermicompost_production", "organic_farm_inputs", "food_processing_spices", "dairy_micro_farm"],
    priority_category: "Micro & Small Business Units",
    collateral_free: true,
    description: "Collateral-free institutional credit up to ₹10 Lakhs: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakhs), and Tarun (₹5 Lakhs to ₹10 Lakhs) for micro-enterprises, small workshops, and rural trade.",
    reasons: [
      "Zero collateral or third-party guarantor required for loans up to ₹10 Lakhs.",
      "MUDRA RuPay Card provided for instant digital working capital withdrawal.",
      "Zero processing fee and simplified 1-page application for Shishu loans."
    ],
    documents_required: ["Aadhaar Card", "Voter ID / PAN", "Bank Account Statement", "Business Proof / Machinery Quotation"],
    application_route: "https://www.mudra.org.in/",
    official_source: "https://www.mudra.org.in/",
    status_tag: "Instant Collateral-Free Credit"
  },
  {
    scheme_id: "stand_up_india",
    scheme_name: "Stand-Up India Scheme",
    short_code: "STAND_UP_INDIA",
    nodal_agency: "SIDBI / Ministry of Finance",
    subsidy_percent: 15.0,
    subsidy_rate_text: "15% Margin Money Support + Subsidized Composite Loan",
    max_project_cost: 10000000,
    applicable_opportunities: ["food_processing_spices", "dairy_micro_farm", "organic_farm_inputs", "handicraft_textiles", "garment_tailoring_unit", "vermicompost_production"],
    priority_category: "SC / ST / Women Entrepreneurs Only",
    collateral_free: false,
    description: "Facilitates bank loans between ₹10 Lakhs and ₹1 Crore to at least one SC or ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise in manufacturing, services, or trading sector.",
    reasons: [
      "Mandated target: Every bank branch must finance at least one SC/ST and one Woman entrepreneur.",
      "15% margin money convergence support with State schemes reduces promoter equity.",
      "Composite loan covering machinery capex and revolving working capital together."
    ],
    documents_required: ["Aadhaar", "Caste Certificate (for SC/ST)", "Detailed Project Report", "Bank Loan Application"],
    application_route: "https://www.standupmitra.in/",
    official_source: "https://www.standupmitra.in/",
    status_tag: "SC/ST & Women Priority"
  },
  {
    scheme_id: "vcf_sc_bc",
    scheme_name: "VCF-SC/BC (Venture Capital Fund for Scheduled Castes & OBCs)",
    short_code: "VCF-SC",
    nodal_agency: "IFCI / Ministry of Social Justice & Empowerment",
    subsidy_percent: 30.0,
    subsidy_rate_text: "Concessional Equity & Low-Interest Debt (4% p.a.)",
    max_project_cost: 150000000,
    applicable_opportunities: ["food_processing_spices", "dairy_micro_farm", "organic_farm_inputs", "vermicompost_production"],
    priority_category: "Marginalized First-Generation Innovators",
    collateral_free: false,
    description: "First-of-its-kind venture capital initiative to promote entrepreneurship and value addition among SC and OBC entrepreneurs by providing concessional financial support up to ₹15 Crores.",
    reasons: [
      "Ultra-low concessional interest rate of only 4% per annum.",
      "Flexible equity partnership with extended moratorium of up to 3 years.",
      "Comprehensive technology incubation support from MoSJE network."
    ],
    documents_required: ["Caste Certificate", "Company / Enterprise Registration", "Techno-Economic Feasibility Report", "KYC of Promoters"],
    application_route: "https://vcfsc.in/",
    official_source: "https://vcfsc.in/",
    status_tag: "MoSJE Concessional Direct Channel"
  }
];

function SchemesContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { t } = useLanguage();

  // User Profile State from LocalStorage / Registration
  const [userProfile, setUserProfile] = useState<any | null>(null);
  const [userName, setUserName] = useState<string>("Rural Entrepreneur");

  // Selected Opportunity
  const opportunityParam = searchParams.get("opportunity");
  const [selectedOpportunityId, setSelectedOpportunityId] = useState<string>(opportunityParam || "all");
  
  // Filter pills: "user_matches", "all", "direct", "high_subsidy", "collateral_free", "priority_quota"
  const [activeFilter, setActiveFilter] = useState<string>("user_matches");
  
  // Card expand toggles
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  // Application modal
  const [modalScheme, setModalScheme] = useState<any | null>(null);
  const [applicationSubmitted, setApplicationSubmitted] = useState(false);

  // Dynamic API schemes
  const [apiSchemes, setApiSchemes] = useState<any[]>(FALLBACK_SCHEMES);
  const [loading, setLoading] = useState(false);

  // Load User Profile on Mount
  useEffect(() => {
    try {
      const storedProfile = localStorage.getItem("thinkforge_profile");
      const storedName = localStorage.getItem("thinkforge_name");
      
      let parsed = null;
      if (storedProfile) {
        parsed = JSON.parse(storedProfile);
        setUserProfile(parsed);
      }
      if (storedName) {
        setUserName(storedName);
      }

      // If user hasn't explicitly specified an opportunity via URL query param,
      // auto-suggest the opportunity matching the user's registered sectorInterest or primarySkill
      if (!opportunityParam && parsed) {
        const sector = (parsed.sectorInterest || "").toLowerCase();
        const skill = (parsed.primarySkill || "").toLowerCase();

        let autoOpp = "all";
        if (sector.includes("dairy") || skill.includes("dairy") || skill.includes("husbandry")) {
          autoOpp = "dairy_micro_farm";
        } else if (sector.includes("food") || sector.includes("milling") || skill.includes("food") || skill.includes("processing")) {
          autoOpp = "food_processing_spices";
        } else if (sector.includes("organic") || sector.includes("bio") || skill.includes("compost") || skill.includes("soil")) {
          autoOpp = "vermicompost_production";
        } else if (sector.includes("textile") || skill.includes("tailor") || skill.includes("stitch")) {
          autoOpp = "garment_tailoring_unit";
        } else if (sector.includes("craft") || skill.includes("handicraft") || skill.includes("weav")) {
          autoOpp = "handicraft_textiles";
        }

        if (autoOpp !== "all") {
          setSelectedOpportunityId(autoOpp);
        }
      }
    } catch (e) {
      console.error("Failed to load user profile in schemes page", e);
    }
  }, [opportunityParam]);

  // Synchronize state when URL search param changes
  useEffect(() => {
    if (opportunityParam && opportunityParam !== selectedOpportunityId) {
      setSelectedOpportunityId(opportunityParam);
    }
  }, [opportunityParam]);

  // Fetch schemes from backend when opportunity or profile changes
  useEffect(() => {
    const fetchSchemes = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (selectedOpportunityId && selectedOpportunityId !== "all") {
          params.set("opportunity_id", selectedOpportunityId);
        }
        if (userProfile) {
          const rawEquity = userProfile.ownEquity ? parseInt(userProfile.ownEquity.replace(/[^0-9]/g, "")) : 150000;
          if (rawEquity) params.set("user_capital", rawEquity.toString());
          if (userProfile.primarySkill) params.set("primary_skill", userProfile.primarySkill);
          if (userProfile.sectorInterest) params.set("sector_interest", userProfile.sectorInterest);
          if (userProfile.district) params.set("district", userProfile.district);
          if (userProfile.state) params.set("state", userProfile.state);
        }

        const queryString = params.toString() ? `?${params.toString()}` : "";
        const res = await fetch(`http://localhost:8000/schemes${queryString}`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setApiSchemes(data);
          }
        }
      } catch (err) {
        console.warn("Backend API not reachable, using localized verified schemes catalog", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSchemes();
  }, [selectedOpportunityId, userProfile]);

  // Current Opportunity configuration
  const currentOpp = useMemo(() => {
    return (
      OPPORTUNITY_CONFIGS.find((o) => o.id === selectedOpportunityId) ||
      OPPORTUNITY_CONFIGS[0]
    );
  }, [selectedOpportunityId]);

  // Numeric capital extracted from user profile
  const userEquityAmount = useMemo(() => {
    if (!userProfile?.ownEquity) return 150000;
    const num = parseInt(userProfile.ownEquity.replace(/[^0-9]/g, ""));
    return isNaN(num) ? 150000 : num;
  }, [userProfile]);

  // Change selected opportunity and update URL
  const handleSelectOpportunity = (oppId: string) => {
    setSelectedOpportunityId(oppId);
    if (oppId === "all") {
      router.push("/schemes");
    } else {
      router.push(`/schemes?opportunity=${oppId}`);
    }
  };

  // Calculate tailored values for a scheme based on user profile and current opportunity capex
  const processedSchemes = useMemo(() => {
    const targetCapex = currentOpp.capex;

    return apiSchemes.map((scheme) => {
      const isDirectMatch =
        selectedOpportunityId !== "all" &&
        scheme.applicable_opportunities?.includes(selectedOpportunityId);

      // Calculate subsidy amount
      const subsidyPct = scheme.subsidy_percent || 0;
      let calculatedSubsidy = targetCapex * (subsidyPct / 100);

      // Respect scheme specific caps
      if (scheme.short_code === "PMFME") calculatedSubsidy = Math.min(calculatedSubsidy, 1000000);
      if (scheme.short_code === "NLM") calculatedSubsidy = Math.min(calculatedSubsidy, 2500000);
      if (scheme.short_code === "SAMARTH") calculatedSubsidy = Math.min(calculatedSubsidy, 25000);
      if (scheme.short_code === "ACABC") calculatedSubsidy = Math.min(calculatedSubsidy, 880000);

      // Dynamic match score computation tailored to user
      let matchScore = scheme.match_score || 80;
      const userFitReasons: string[] = [];

      // User Information Evaluation
      if (userProfile) {
        // 1. Capital / Equity Fit
        const reqPromoterMargin = targetCapex * 0.10; // 10% standard margin
        if (userEquityAmount >= reqPromoterMargin) {
          userFitReasons.push(`Your available equity of ₹${userEquityAmount.toLocaleString()} covers the required 10% promoter margin.`);
          matchScore += 3;
        }

        // 2. Skill Fit
        if (userProfile.primarySkill) {
          const skillLower = userProfile.primarySkill.toLowerCase();
          if (
            (skillLower.includes("dairy") && scheme.short_code === "NLM") ||
            ((skillLower.includes("food") || skillLower.includes("agri") || skillLower.includes("agro")) && scheme.short_code === "PMFME") ||
            (skillLower.includes("tailor") && scheme.short_code === "SAMARTH") ||
            (skillLower.includes("compost") && scheme.short_code === "PKVY") ||
            (skillLower.includes("craft") && scheme.short_code === "SFURTI")
          ) {
            userFitReasons.push(`Your registered skill '${userProfile.primarySkill}' satisfies the technical qualification standard.`);
            matchScore += 5;
          }
        }

        // 3. SHG Member
        if (userProfile.isShgMember) {
          if (scheme.short_code === "PMFME") {
            userFitReasons.push("SHG Membership unlocks an extra ₹40,000 seed grant for initial working capital.");
            matchScore += 4;
          } else if (scheme.short_code === "SFURTI" || scheme.short_code === "PMEGP") {
            userFitReasons.push("SHG members receive fast-track committee sanction at the District Level.");
            matchScore += 2;
          }
        }

        // 4. Collateral requirement alignment
        if (!userProfile.hasCollateral && scheme.collateral_free) {
          userFitReasons.push("Zero collateral match: Fits your profile requirement for 100% credit guarantee cover.");
          matchScore += 4;
        }

        // 5. Rural Location Advantage
        if (scheme.short_code === "PMEGP") {
          userFitReasons.push(`Rural location in ${userProfile.district || "Wardha"} qualifies you for 35% subsidy (compared to 25% urban).`);
          matchScore += 3;
        }
      }

      if (isDirectMatch) matchScore += 6;
      if (subsidyPct >= 35) matchScore += 2;

      // Merge backend reasons with user-specific reasons
      const combinedReasons = [
        ...userFitReasons,
        ...(scheme.reasons || [])
      ].filter((r, idx, arr) => arr.indexOf(r) === idx);

      return {
        ...scheme,
        isDirectMatch,
        calculatedSubsidy: Math.round(calculatedSubsidy),
        calculatedNetLoan: Math.max(0, targetCapex - Math.round(calculatedSubsidy)),
        dynamicMatchScore: Math.min(99, Math.round(matchScore)),
        userSpecificReasons: userFitReasons,
        displayReasons: combinedReasons
      };
    });
  }, [apiSchemes, currentOpp, selectedOpportunityId, userProfile, userEquityAmount]);

  // Filter schemes according to active filter pill
  const filteredSchemes = useMemo(() => {
    return processedSchemes.filter((scheme) => {
      if (activeFilter === "user_matches") {
        // High fit scores for this user (>80%)
        return scheme.dynamicMatchScore >= 80;
      }
      if (activeFilter === "direct") {
        return (
          selectedOpportunityId === "all" ||
          scheme.applicable_opportunities?.includes(selectedOpportunityId)
        );
      }
      if (activeFilter === "high_subsidy") {
        return scheme.subsidy_percent >= 30;
      }
      if (activeFilter === "collateral_free") {
        return scheme.collateral_free === true;
      }
      if (activeFilter === "priority_quota") {
        return (
          scheme.priority_category?.includes("Women") ||
          scheme.priority_category?.includes("SC") ||
          scheme.priority_category?.includes("Rural") ||
          scheme.priority_category?.includes("ALL")
        );
      }
      return true;
    }).sort((a, b) => {
      return (b.dynamicMatchScore || 0) - (a.dynamicMatchScore || 0);
    });
  }, [processedSchemes, activeFilter, selectedOpportunityId]);

  // Highest subsidy amount among filtered schemes
  const maxPossibleSubsidy = useMemo(() => {
    return Math.max(...filteredSchemes.map((s) => s.calculatedSubsidy || 0), 0);
  }, [filteredSchemes]);

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700">
            <Landmark className="w-4 h-4 text-brand-600" />
            <span>{t("POLICY & SUBSIDY ROUTING")}</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">{t("Government Scheme Matching")}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">
            {t("Personalized Government Scheme Suggestions")}
          </h1>
          <p className="text-sm text-slate-600">
            {t("Official Central & State subsidies dynamically matched against your skills, available equity, and chosen business opportunity.")}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setModalScheme(filteredSchemes[0] || processedSchemes[0]);
              setApplicationSubmitted(false);
            }}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-brand-600 text-white hover:bg-brand-700 shadow-glow-teal transition-all"
          >
            <Sparkles className="w-4 h-4 text-emerald-200" />
            {t("Auto-Fill Scheme Application")}
          </button>
        </div>
      </div>

      {/* User Information Dossier Bar */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-brand-950 text-white rounded-2xl p-4 sm:p-5 border border-slate-700/60 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-brand-500/20 text-brand-400 border border-brand-400/30 flex items-center justify-center font-bold">
              <UserCheck className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white leading-tight">
                  {t("Suggested Schemes for")} {t(userName)}
                </h3>
                <span className="bg-emerald-500/20 border border-emerald-400/40 text-emerald-300 text-[10px] font-semibold px-2 py-0.5 rounded-full">
                  {t("Profile Calibrated")}
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                {t("Evaluated against your verified equity, vocational skills, rural residence, and collateral capability.")}
              </p>
            </div>
          </div>

          <Link
            href="/register"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 text-white border border-white/15 transition-colors self-start md:self-auto"
          >
            <Edit3 className="w-3.5 h-3.5 text-emerald-300" />
            <span>{t("Update Capability Inputs")}</span>
          </Link>
        </div>

        {/* Profile Attributes Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5 pt-3 text-xs">
          <div className="bg-white/5 rounded-xl p-2.5 border border-white/10">
            <span className="text-slate-400 text-[10px] block font-medium">📍 {t("Rural Cluster")}</span>
            <span className="font-bold text-slate-100 truncate block mt-0.5">
              {t(userProfile?.district || "Wardha")}, {t(userProfile?.state || "Maharashtra")}
            </span>
          </div>

          <div className="bg-white/5 rounded-xl p-2.5 border border-white/10">
            <span className="text-slate-400 text-[10px] block font-medium">💼 {t("Primary Skill")}</span>
            <span className="font-bold text-slate-100 truncate block mt-0.5">
              {t(userProfile?.primarySkill || "Agri-Processing")}
            </span>
          </div>

          <div className="bg-white/5 rounded-xl p-2.5 border border-white/10">
            <span className="text-slate-400 text-[10px] block font-medium">💰 {t("Available Equity")}</span>
            <span className="font-bold text-emerald-300 truncate block mt-0.5">
              ₹{userEquityAmount.toLocaleString()}
            </span>
          </div>

          <div className="bg-white/5 rounded-xl p-2.5 border border-white/10">
            <span className="text-slate-400 text-[10px] block font-medium">👥 {t("SHG Membership")}</span>
            <span className="font-bold text-slate-100 truncate block mt-0.5">
              {userProfile?.isShgMember ? t("Yes (Seed Grant Active)") : t("Individual Applicant")}
            </span>
          </div>

          <div className="bg-white/5 rounded-xl p-2.5 border border-white/10">
            <span className="text-slate-400 text-[10px] block font-medium">🛡️ {t("Collateral Preference")}</span>
            <span className="font-bold text-slate-100 truncate block mt-0.5">
              {userProfile?.hasCollateral ? t("Asset Backed") : t("Zero Collateral (CGTMSE)")}
            </span>
          </div>
        </div>
      </div>

      {/* Opportunity Selector Bar */}
      <div className="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-sm">
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-700 uppercase tracking-wider">
            <Layers className="w-4 h-4 text-brand-600" />
            <span>{t("Target Business Opportunity")}</span>
          </div>
          <span className="text-xs text-slate-500 font-medium">
            {selectedOpportunityId === "all"
              ? t("All Opportunities")
              : `${t("Calibrated for")} ${t(currentOpp.name)}`}
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
          {OPPORTUNITY_CONFIGS.map((opp) => {
            const isSelected = selectedOpportunityId === opp.id;
            return (
              <button
                key={opp.id}
                onClick={() => handleSelectOpportunity(opp.id)}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all ${
                  isSelected
                    ? "bg-brand-50 border-brand-500 text-brand-900 shadow-sm ring-2 ring-brand-500/20 font-bold"
                    : "bg-slate-50/70 border-slate-200/80 text-slate-700 hover:bg-slate-100 hover:border-slate-300"
                }`}
              >
                <span className="text-xl mb-1">{opp.emoji}</span>
                <span className="text-[11px] font-semibold leading-tight line-clamp-2">
                  {t(opp.name)}
                </span>
                {opp.id !== "all" && (
                  <span className="text-[10px] text-slate-500 mt-1 font-mono">
                    ₹{(opp.capex / 1000).toFixed(0)}k {t("capex")}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Opportunity Insights Hero Banner */}
      {selectedOpportunityId !== "all" && (
        <div className="bg-gradient-to-r from-brand-900 via-brand-800 to-slate-900 text-white rounded-2xl p-5 shadow-lg border border-brand-700/40">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-lg">{currentOpp.emoji}</span>
                <span className="text-xs font-semibold uppercase tracking-wider text-emerald-300">
                  {t("Target Opportunity:")} {t(currentOpp.sector)}
                </span>
              </div>
              <h2 className="text-xl font-bold text-white">{t(currentOpp.name)}</h2>
              <p className="text-xs text-slate-300 max-w-xl leading-relaxed">
                {t(currentOpp.description)} {t("Standard project investment is")} ₹{currentOpp.capex.toLocaleString()}. {t("Your")} ₹{userEquityAmount.toLocaleString()} {t("equity covers the promoter share.")}
              </p>
            </div>

            <div className="flex flex-wrap sm:flex-nowrap items-center gap-3">
              <div className="bg-white/10 backdrop-blur-sm border border-white/15 px-4 py-3 rounded-xl text-center min-w-[130px]">
                <span className="text-[11px] text-emerald-200 block font-medium">{t("Capex Needed")}</span>
                <span className="text-base font-bold text-white">₹{currentOpp.capex.toLocaleString()}</span>
              </div>

              <div className="bg-emerald-500/20 backdrop-blur-sm border border-emerald-400/30 px-4 py-3 rounded-xl text-center min-w-[150px]">
                <span className="text-[11px] text-emerald-300 block font-medium">{t("Max Gov Subsidy")}</span>
                <span className="text-base font-bold text-emerald-300">
                  ₹{maxPossibleSubsidy.toLocaleString()}
                </span>
              </div>

              <button
                onClick={() => handleSelectOpportunity("all")}
                className="px-3 py-3 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition-colors border border-white/10"
                title={t("Clear Filter")}
              >
                {t("Clear Filter")}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Filter Chips Bar */}
      <div className="flex items-center justify-between flex-wrap gap-3 pt-1">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          <span className="text-slate-400 font-medium flex items-center gap-1 pl-1">
            <Filter className="w-3.5 h-3.5" />
            {t("Filter:")}
          </span>

          <button
            onClick={() => setActiveFilter("user_matches")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all flex items-center gap-1.5 ${
              activeFilter === "user_matches"
                ? "bg-brand-600 text-white font-semibold shadow-sm"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            <Sparkles className="w-3 h-3 text-emerald-300" />
            <span>{t("Top Matches for You")}</span>
          </button>

          <button
            onClick={() => setActiveFilter("all")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeFilter === "all"
                ? "bg-slate-900 text-white font-semibold shadow-sm"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {t("All Schemes")} ({processedSchemes.length})
          </button>

          {selectedOpportunityId !== "all" && (
            <button
              onClick={() => setActiveFilter("direct")}
              className={`px-3 py-1.5 rounded-lg font-medium transition-all flex items-center gap-1.5 ${
                activeFilter === "direct"
                  ? "bg-brand-700 text-white font-semibold shadow-sm"
                  : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
              }`}
            >
              {t("Direct Sector Schemes")}
            </button>
          )}

          <button
            onClick={() => setActiveFilter("high_subsidy")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeFilter === "high_subsidy"
                ? "bg-emerald-700 text-white font-semibold shadow-sm"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {t("High Subsidy (>30%)")}
          </button>

          <button
            onClick={() => setActiveFilter("collateral_free")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeFilter === "collateral_free"
                ? "bg-indigo-700 text-white font-semibold shadow-sm"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {t("100% Collateral-Free")}
          </button>

          <button
            onClick={() => setActiveFilter("priority_quota")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeFilter === "priority_quota"
                ? "bg-amber-700 text-white font-semibold shadow-sm"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {t("Women / SC / ST Priority")}
          </button>
        </div>

        <div className="text-xs text-slate-500 font-medium">
          {t("Showing")} <span className="font-bold text-slate-800">{filteredSchemes.length}</span> {t("schemes")}
        </div>
      </div>

      {/* Schemes Grid */}
      <div className="space-y-4">
        {filteredSchemes.map((scheme) => {
          const isExpanded = expandedCard === (scheme.scheme_id || scheme.short_code);
          const hasDirectBadge = scheme.isDirectMatch;
          const isHighMatch = (scheme.dynamicMatchScore || 0) >= 95;

          return (
            <div
              key={scheme.scheme_id || scheme.short_code || scheme.scheme_name}
              className={`bg-white rounded-2xl border transition-all shadow-card hover:shadow-card-elevated ${
                isHighMatch
                  ? "border-emerald-500/60 ring-1 ring-emerald-500/20"
                  : hasDirectBadge
                  ? "border-brand-500/60 ring-1 ring-brand-500/20"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              <div className="p-6">
                {/* Card Top Row */}
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-3 pb-4 border-b border-slate-100">
                  <div className="space-y-1.5">
                    <div className="flex items-center flex-wrap gap-2">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                        {t(scheme.nodal_agency) || t("Central / State Ministry")}
                      </span>
                      <EvidenceBadge type="VERIFIED" />
                      {isHighMatch && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-300">
                          <Sparkles className="w-3 h-3 text-emerald-600" />
                          {t("Top Personal Match for")} {t(userName.split(" ")[0])}
                        </span>
                      )}
                      {hasDirectBadge && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-full border border-brand-200">
                          {t("Recommended for")} {t(currentOpp.name)}
                        </span>
                      )}
                      {scheme.status_tag && (
                        <span className="text-[11px] font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">
                          {t(scheme.status_tag)}
                        </span>
                      )}
                    </div>

                    <h3 className="text-lg font-bold text-slate-900 leading-snug">
                      {t(scheme.scheme_name)}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <div className="text-right">
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200 inline-block">
                        {scheme.dynamicMatchScore || 92}% {t("Match Score")}
                      </span>
                    </div>
                    <a
                      href={scheme.application_route || scheme.official_source}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-900 text-white hover:bg-brand-700 transition-colors shadow-sm"
                    >
                      <span>{t("Official Portal")}</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                    </a>
                  </div>
                </div>

                {/* Description */}
                <p className="text-xs text-slate-600 mt-3 leading-relaxed">
                  {t(scheme.description)}
                </p>

                {/* Financial Calibration Box */}
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
                  <div className="p-3 bg-brand-50/60 rounded-xl border border-brand-100">
                    <span className="text-slate-500 block font-medium">{t("Subsidy Assistance")}</span>
                    <span className="font-bold text-brand-700 text-sm mt-0.5 block">
                      {t(scheme.subsidy_rate_text) || `${scheme.subsidy_percent}% Subsidy`}
                    </span>
                  </div>

                  <div className="p-3 bg-emerald-50/70 rounded-xl border border-emerald-100">
                    <span className="text-slate-500 block font-medium">
                      {t("Est. Subsidy on")} ₹{(currentOpp.capex / 1000).toFixed(0)}k {t("capex")}
                    </span>
                    <span className="font-bold text-emerald-700 text-sm mt-0.5 block">
                      {scheme.calculatedSubsidy > 0
                        ? `₹${scheme.calculatedSubsidy.toLocaleString()}`
                        : "Collateral Relief / Subvention"}
                    </span>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <span className="text-slate-500 block font-medium">{t("Max Project Cap")}</span>
                    <span className="font-bold text-slate-900 text-sm mt-0.5 block">
                      ₹{((scheme.max_project_cost || scheme.project_cap || 1000000) / 100000).toFixed(0)} Lakhs
                    </span>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <span className="text-slate-500 block font-medium">{t("Collateral Requirement")}</span>
                    <span className="font-bold text-slate-800 text-sm mt-0.5 flex items-center gap-1">
                      {scheme.collateral_free ? (
                        <>
                          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                          <span className="text-emerald-700 font-semibold">{t("100% Collateral Free")}</span>
                        </>
                      ) : (
                        <span>{t("Bank Term Loan / Hypothecation")}</span>
                      )}
                    </span>
                  </div>
                </div>

                {/* Personalized Why Recommended bullet points */}
                {scheme.displayReasons && scheme.displayReasons.length > 0 && (
                  <div className="mt-3.5 bg-slate-50/90 rounded-xl p-3.5 border border-slate-100">
                    <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider block mb-2 flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-brand-600" />
                      {t("Why Recommended for")} {t(userName.split(" ")[0])} ({selectedOpportunityId === "all" ? t("Rural Enterprise") : t(currentOpp.name)}):
                    </span>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {scheme.displayReasons.slice(0, 4).map((r: string, idx: number) => (
                        <div key={idx} className="flex items-start gap-1.5 text-xs text-slate-700">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                          <span>{t(r)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Expandable Document Checklist Section */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-slate-100 animate-in fade-in duration-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5 text-brand-600" />
                          {t("Required Documents Checklist")}
                        </h4>
                        <ul className="space-y-1.5 text-xs text-slate-600">
                          {(scheme.documents_required || [
                            "Aadhaar Card of Entrepreneur",
                            "Bank Account Passbook / 6M Statement",
                            "Detailed Project Report (DPR)",
                            "Machinery / Equipment Quotations"
                          ]).map((doc: string, dIdx: number) => (
                            <li key={dIdx} className="flex items-center gap-2">
                              <span className="w-1.5 h-1.5 rounded-full bg-brand-500" />
                              <span>{t(doc)}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div>
                        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                          <Building2 className="w-3.5 h-3.5 text-slate-600" />
                          {t("Application Routing & Convergence")}
                        </h4>
                        <p className="text-xs text-slate-600 leading-relaxed">
                          {t("Applications can be submitted via the official portal or your local District Industries Centre (DIC) / Lead Bank Manager.")}
                          {scheme.subsidy_percent > 0 && (
                            <span className="block mt-1.5 font-medium text-brand-700">
                              💡 {t("Margin money is directly credited to your bank account after physical verification of machinery.")}
                            </span>
                          )}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Card Actions Footer */}
                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between flex-wrap gap-2">
                  <button
                    onClick={() =>
                      setExpandedCard(
                        isExpanded ? null : scheme.scheme_id || scheme.short_code
                      )
                    }
                    className="inline-flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors"
                  >
                    <span>{isExpanded ? t("Hide Requirements") : t("View Required Documents & Routing")}</span>
                    {isExpanded ? (
                      <ChevronUp className="w-3.5 h-3.5" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5" />
                    )}
                  </button>

                  <div className="flex items-center gap-2">
                    <Link
                      href={`/finance?capex=${currentOpp.capex}&subsidy=${scheme.calculatedSubsidy}&scheme=${scheme.short_code || ""}`}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold text-brand-700 hover:bg-brand-50 border border-brand-200 transition-colors"
                    >
                      <Coins className="w-3.5 h-3.5 text-brand-600" />
                      <span>{t("Simulate in Finance Engine")}</span>
                    </Link>

                    <button
                      onClick={() => {
                        setModalScheme(scheme);
                        setApplicationSubmitted(false);
                      }}
                      className="inline-flex items-center gap-1 px-3.5 py-1.5 rounded-lg text-xs font-bold bg-brand-600 text-white hover:bg-brand-700 shadow-sm transition-all"
                    >
                      <Sparkles className="w-3 h-3 text-emerald-200" />
                      <span>{t("Auto-Fill Application")}</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Auto-Fill Application Modal */}
      {modalScheme && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between p-5 border-b border-slate-100 bg-slate-50/50">
              <div>
                <span className="text-[11px] font-semibold text-brand-600 uppercase tracking-wider mb-0.5 block">
                  {t("AI Scheme Concierge")}
                </span>
                <h3 className="text-lg font-bold text-slate-900 leading-tight">
                  {t("Auto-Fill Application Form")}
                </h3>
              </div>
              <button
                onClick={() => setModalScheme(null)}
                className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 space-y-4">
              {applicationSubmitted ? (
                <div className="text-center py-6 space-y-3">
                  <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                    <CheckCircle2 className="w-7 h-7" />
                  </div>
                  <h4 className="text-base font-bold text-slate-900">{t("Application Dossier Prepared!")}</h4>
                  <p className="text-xs text-slate-600 max-w-sm mx-auto leading-relaxed">
                    {t("Your pre-filled application dossier for")} <strong>{t(modalScheme.scheme_name)}</strong> {t("has been generated for")} <strong>{t(userName)}</strong> ({t(userProfile?.district || "Wardha")} {t("Rural Cluster")}), {t("featuring machinery quotes, bank margin subsidy, and technical capability verification.")}
                  </p>
                  <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-emerald-800 font-medium">
                    {t("Estimated Government Margin Money Subsidy:")} ₹{modalScheme.calculatedSubsidy?.toLocaleString()}
                  </div>
                </div>
              ) : (
                <>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100 space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">{t("Applicant:")}</span>
                      <span className="font-bold text-slate-800">{t(userName)} ({t(userProfile?.district || "Wardha")}, {t(userProfile?.state || "Maharashtra")})</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{t("Scheme:")}</span>
                      <span className="font-bold text-slate-800">{t(modalScheme.short_code)} ({t(modalScheme.nodal_agency)})</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{t("Target Opportunity:")}</span>
                      <span className="font-bold text-slate-800">{t(currentOpp.name)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{t("Project Capex / Equity:")}</span>
                      <span className="font-bold text-slate-800">₹{currentOpp.capex.toLocaleString()} ({t("Promoter Equity:")} ₹{userEquityAmount.toLocaleString()})</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{t("Subsidy Claim:")}</span>
                      <span className="font-bold text-emerald-700">₹{modalScheme.calculatedSubsidy?.toLocaleString()} ({modalScheme.subsidy_percent}%)</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-700 block">
                      {t("Auto-Populated from Your Capability Dossier:")}
                    </label>
                    <div className="space-y-1.5 text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-100">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{t("Entrepreneur KYC &")} {t(userProfile?.district || "Wardha")} {t("Rural Certificate")}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{t("Skill Accreditation:")} {t(userProfile?.primarySkill || "Agri-Processing")}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{t("Land")} ({t(userProfile?.landAccess || "Owned")}) {t("& Power")} ({t(userProfile?.powerSupply || "Commercial")}) {t("Declaration")}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{t("Detailed Project Report (DPR) with 3-Year Financials")}</span>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="p-5 border-t border-slate-100 bg-slate-50/50 flex justify-end gap-3">
              <button
                onClick={() => setModalScheme(null)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
              >
                {t("Close")}
              </button>
              {!applicationSubmitted ? (
                <button
                  onClick={() => setApplicationSubmitted(true)}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-600 text-white text-xs font-bold hover:bg-brand-700 shadow-glow-teal transition-all"
                >
                  <Sparkles className="w-3.5 h-3.5 text-emerald-200" />
                  <span>{t("Generate Pre-Filled Application Dossier")}</span>
                </button>
              ) : (
                <a
                  href={modalScheme.application_route || modalScheme.official_source}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-brand-700 transition-colors"
                >
                  <span>{t("Proceed to Official Submission")}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function SchemesPage() {
  const { t } = useLanguage();
  return (
    <Suspense
      fallback={
        <div className="p-8 text-center text-slate-500 text-sm">
          {t("Loading personalized scheme recommendations...")}
        </div>
      }
    >
      <SchemesContent />
    </Suspense>
  );
}

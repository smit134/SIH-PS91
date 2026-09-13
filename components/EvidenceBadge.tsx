import React from "react";
import { CheckCircle2, Calculator, HelpCircle, Sparkles } from "lucide-react";
import clsx from "clsx";
import { useLanguage } from "@/contexts/LanguageContext";

export type EvidenceType = "VERIFIED" | "DERIVED" | "ESTIMATED" | "UNKNOWN";

interface EvidenceBadgeProps {
  type: EvidenceType;
  className?: string;
  showIcon?: boolean;
}

const badgeConfig: Record<EvidenceType, { labelKey: string; icon: React.ElementType; classes: string; descKey: string }> = {
  VERIFIED: {
    labelKey: "dash_evidence_verified",
    icon: CheckCircle2,
    classes: "bg-emerald-500/10 text-emerald-700 border-emerald-500/25 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800",
    descKey: "ev_desc_verified",
  },
  DERIVED: {
    labelKey: "dash_evidence_derived",
    icon: Calculator,
    classes: "bg-brand-500/10 text-brand-700 border-brand-500/25 dark:bg-brand-950/40 dark:text-brand-300 dark:border-brand-800",
    descKey: "ev_desc_derived",
  },
  ESTIMATED: {
    labelKey: "dash_evidence_estimated",
    icon: Sparkles,
    classes: "bg-amber-500/10 text-amber-700 border-amber-500/25 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800",
    descKey: "ev_desc_estimated",
  },
  UNKNOWN: {
    labelKey: "prof_unknown",
    icon: HelpCircle,
    classes: "bg-slate-500/10 text-slate-700 border-slate-500/25 dark:bg-slate-800/60 dark:text-slate-300 dark:border-slate-700",
    descKey: "ev_desc_unknown",
  },
};

export const EvidenceBadge: React.FC<EvidenceBadgeProps> = ({
  type,
  className,
  showIcon = true,
}) => {
  const { t } = useLanguage();
  const config = badgeConfig[type] || badgeConfig.UNKNOWN;
  const Icon = config.icon;

  return (
    <span
      title={t(config.descKey)}
      className={clsx(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide border transition-colors",
        config.classes,
        className
      )}
    >
      {showIcon && <Icon className="w-3.5 h-3.5 shrink-0" />}
      <span>{t(config.labelKey)}</span>
    </span>
  );
};

export default EvidenceBadge;

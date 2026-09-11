import React from "react";
import { CheckCircle2, Calculator, HelpCircle, Sparkles } from "lucide-react";
import clsx from "clsx";

export type EvidenceType = "VERIFIED" | "DERIVED" | "ESTIMATED" | "UNKNOWN";

interface EvidenceBadgeProps {
  type: EvidenceType;
  className?: string;
  showIcon?: boolean;
}

const badgeConfig: Record<EvidenceType, { label: string; icon: React.ElementType; classes: string; desc: string }> = {
  VERIFIED: {
    label: "VERIFIED",
    icon: CheckCircle2,
    classes: "bg-emerald-500/10 text-emerald-700 border-emerald-500/25 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800",
    desc: "Ground-truth data from official records & mandi registers",
  },
  DERIVED: {
    label: "DERIVED",
    icon: Calculator,
    classes: "bg-brand-500/10 text-brand-700 border-brand-500/25 dark:bg-brand-950/40 dark:text-brand-300 dark:border-brand-800",
    desc: "Computed through validated economic algorithms & benchmarks",
  },
  ESTIMATED: {
    label: "ESTIMATED",
    icon: Sparkles,
    classes: "bg-amber-500/10 text-amber-700 border-amber-500/25 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800",
    desc: "Regional statistical heuristic and cluster projection",
  },
  UNKNOWN: {
    label: "UNKNOWN",
    icon: HelpCircle,
    classes: "bg-slate-500/10 text-slate-700 border-slate-500/25 dark:bg-slate-800/60 dark:text-slate-300 dark:border-slate-700",
    desc: "Data pending local ground survey or entrepreneur verification",
  },
};

export const EvidenceBadge: React.FC<EvidenceBadgeProps> = ({
  type,
  className,
  showIcon = true,
}) => {
  const config = badgeConfig[type] || badgeConfig.UNKNOWN;
  const Icon = config.icon;

  return (
    <span
      title={config.desc}
      className={clsx(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide border transition-colors",
        config.classes,
        className
      )}
    >
      {showIcon && <Icon className="w-3.5 h-3.5 shrink-0" />}
      <span>{config.label}</span>
    </span>
  );
};

export default EvidenceBadge;

import { OpportunityChart } from '@/components/charts/OpportunityChart';
import { CapabilityScorecard } from '@/components/charts/CapabilityScorecard';
import { CostBreakdownChart, CashFlowChart } from '@/components/charts/FinancialCharts';
import { ScenarioSimulator } from '@/components/simulator/ScenarioSimulator';
import { HyperLocalMap } from '@/components/map/HyperLocalMap';
import { BlueprintExport } from '@/components/pdf/BlueprintExport';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        
        <header className="mb-8">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">ThinkForge Visualizations</h1>
          <p className="text-slate-500 mt-2 text-lg">Preview of components built by Harshanshu.</p>
        </header>

        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">1. Visualizations (Recharts)</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <OpportunityChart />
            <CapabilityScorecard />
            <CostBreakdownChart />
            <CashFlowChart />
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">2. Hyper-Local Map Dashboard</h2>
          <HyperLocalMap />
        </section>

        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">3. Scenario Simulator</h2>
          <ScenarioSimulator />
        </section>

        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">4. PDF Generation UI</h2>
          <BlueprintExport />
        </section>

      </div>
    </main>
  );
}

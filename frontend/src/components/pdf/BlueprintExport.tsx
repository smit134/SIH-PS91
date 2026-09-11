"use client";

import React, { useRef, useState } from 'react';
import { Download, Loader2 } from 'lucide-react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

export function BlueprintExport() {
  const [isExporting, setIsExporting] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  const handleExport = async () => {
    if (!reportRef.current) return;
    setIsExporting(true);
    
    try {
      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        useCORS: true,
        logging: false,
      });
      
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save('ThinkForge_Business_Blueprint.pdf');
    } catch (error) {
      console.error('Failed to generate PDF:', error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Final Business Blueprint</h2>
        <button
          onClick={handleExport}
          disabled={isExporting}
          className="flex items-center space-x-2 bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg shadow-sm transition-colors disabled:opacity-50"
        >
          {isExporting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
          <span>{isExporting ? 'Generating PDF...' : 'Download Blueprint'}</span>
        </button>
      </div>
      
      {/* Printable Report Area */}
      <div 
        ref={reportRef} 
        className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm"
        style={{ minHeight: '800px' }}
      >
        <div className="border-b border-slate-200 pb-6 mb-6 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-1">Business Blueprint</h1>
            <p className="text-slate-500">ThinkForge AI Decision Support System</p>
          </div>
          <div className="text-right">
            <p className="font-semibold text-teal-600 text-xl">Handicraft Products</p>
            <p className="text-sm text-slate-500">Business Fit: 89/100</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-slate-800 mb-3 border-b pb-2">Local Opportunity</h3>
            <ul className="space-y-2 text-sm text-slate-700">
              <li><span className="font-medium">Market Signal:</span> Medium</li>
              <li><span className="font-medium">Price Evidence:</span> Strong</li>
              <li><span className="font-medium">Competitors:</span> 11 (5km radius)</li>
              <li><span className="font-medium">Evidence Coverage:</span> 68%</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-slate-800 mb-3 border-b pb-2">Financial Structure</h3>
            <ul className="space-y-2 text-sm text-slate-700">
              <li><span className="font-medium">Project Cost:</span> ₹2,00,000</li>
              <li><span className="font-medium">Capital Required:</span> ₹80,000</li>
              <li><span className="font-medium">Est. Monthly Profit:</span> ₹23,000</li>
              <li><span className="font-medium">Break-even:</span> 11 months</li>
            </ul>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="font-bold text-slate-800 mb-3 border-b pb-2">Partner Recommendations</h3>
          <div className="bg-slate-50 p-4 rounded border border-slate-100">
            <p className="font-medium text-slate-800">Partner A (94% Synergy)</p>
            <p className="text-sm text-slate-600 mb-2">Fills your Marketing capability gap.</p>
            <div className="flex gap-2">
              <span className="px-2 py-1 bg-teal-100 text-teal-800 text-xs rounded-full">Marketing Skill</span>
              <span className="px-2 py-1 bg-teal-100 text-teal-800 text-xs rounded-full">Capital Available</span>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="font-bold text-slate-800 mb-3 border-b pb-2">Action Plan (Next 7 Days)</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm text-slate-700">
            <li>Contact suppliers for raw material quotes.</li>
            <li>Compare raw material prices locally vs regional market.</li>
            <li>Talk to 5 potential customers to validate demand.</li>
            <li>Connect with Partner A (Marketing).</li>
            <li>Validate selling price (₹500/unit).</li>
            <li>Prepare financing documents for MUDRA scheme.</li>
            <li>Final review of business viability.</li>
          </ol>
        </div>
        
        <div className="mt-12 pt-4 border-t border-slate-200 text-center text-xs text-slate-400">
          Generated by ThinkForge on {new Date().toLocaleDateString()}
        </div>
      </div>
    </div>
  );
}

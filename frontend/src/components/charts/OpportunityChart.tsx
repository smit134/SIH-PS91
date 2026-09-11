"use client";

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface OpportunityData {
  name: string;
  score: number;
}

const data: OpportunityData[] = [
  { name: 'Handicraft', score: 89 },
  { name: 'Dairy', score: 74 },
  { name: 'Food Processing', score: 82 },
  { name: 'Vermicompost', score: 91 },
  { name: 'Organic inputs', score: 84 },
];

export function OpportunityChart() {
  return (
    <div className="w-full h-64 bg-white p-4 rounded-xl shadow-sm border border-slate-100">
      <h3 className="text-lg font-semibold text-slate-800 mb-4">Top Opportunities</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
          <XAxis type="number" domain={[0, 100]} stroke="#64748b" />
          <YAxis dataKey="name" type="category" width={100} stroke="#64748b" fontSize={12} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            cursor={{fill: '#f1f5f9'}}
          />
          <Bar dataKey="score" fill="#0d9488" radius={[0, 4, 4, 0]} barSize={20} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

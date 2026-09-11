"use client";

import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

const data = [
  { subject: 'Production', A: 92, fullMark: 100 },
  { subject: 'Capital', A: 44, fullMark: 100 },
  { subject: 'Marketing', A: 28, fullMark: 100 },
  { subject: 'Distribution', A: 35, fullMark: 100 },
  { subject: 'Technology', A: 61, fullMark: 100 },
  { subject: 'Management', A: 70, fullMark: 100 },
];

export function CapabilityScorecard() {
  return (
    <div className="w-full h-80 bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex flex-col">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">Capability Scorecard</h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#475569', fontSize: 12 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
            <Radar
              name="Entrepreneur"
              dataKey="A"
              stroke="#0d9488"
              fill="#14b8a6"
              fillOpacity={0.4}
            />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-2 text-sm text-slate-600">
        <p className="font-medium text-amber-600 mb-1">Biggest Gaps:</p>
        <ol className="list-decimal list-inside space-y-1">
          <li>Market access (Marketing)</li>
          <li>Working capital (Capital)</li>
          <li>Distribution</li>
        </ol>
      </div>
    </div>
  );
}
